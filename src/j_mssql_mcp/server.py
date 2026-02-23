"""SQL Server MCP Server with Windows Authentication support."""

import os
import pyodbc
from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Any

# Environment configuration
SQL_SERVER = os.getenv("SQL_SERVER", "localhost")
SQL_DATABASE = os.getenv("SQL_DATABASE", "master")
SQL_PORT = os.getenv("SQL_PORT", "1433")

# Connection string with Windows Authentication
CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER},{SQL_PORT};"
    f"DATABASE={SQL_DATABASE};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

app = Server("j-mssql-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available SQL execution tools."""
    return [
        Tool(
            name="execute_sql",
            description="Execute a read-only SQL query on the SQL Server database. "
            "Only SELECT statements are allowed for safety.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute (SELECT only)",
                    }
                },
                "required": ["query"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute SQL queries with safety checks."""
    if name != "execute_sql":
        raise ValueError(f"Unknown tool: {name}")

    query = arguments.get("query", "").strip()

    if not query:
        raise ValueError("Query cannot be empty")

    # Safety check: only allow SELECT statements
    query_upper = query.upper().strip()
    if not query_upper.startswith("SELECT"):
        raise ValueError(
            "Only SELECT statements are allowed. "
            "For data modification, please execute manually through SQL Server Management Studio."
        )

    # Additional safety: block dangerous keywords
    dangerous_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "EXEC",
        "EXECUTE",
    ]
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            raise ValueError(
                f"Query contains forbidden keyword: {keyword}. "
                "Only read-only SELECT statements are allowed."
            )

    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Format results as a table
        if not rows:
            result = "Query executed successfully. No rows returned."
        else:
            # Create header
            result = " | ".join(columns) + "\n"
            result += "-" * len(result) + "\n"

            # Add rows
            for row in rows:
                result += " | ".join(str(value) if value is not None else "NULL" for value in row) + "\n"

            result += f"\n({len(rows)} row(s) returned)"

        return [TextContent(type="text", text=result)]

    except pyodbc.Error as e:
        error_msg = f"Database error: {str(e)}"
        return [TextContent(type="text", text=error_msg)]
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        return [TextContent(type="text", text=error_msg)]


def main():
    """Main entry point for the MCP server."""
    import asyncio
    from mcp.server.stdio import stdio_server

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options(),
            )

    asyncio.run(run())


if __name__ == "__main__":
    main()
