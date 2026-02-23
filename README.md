# j-mssql-mcp

SQL Server MCP Server with Windows Authentication support for Kiro AI.

## Features

- Windows Authentication (Trusted Connection) for SQL Server
- Environment-based configuration
- Read-only query execution for safety
- Supports any SQL Server database with Windows Authentication

## Installation

### Option 1: Direct from GitHub with uvx (Recommended)

No installation needed! Just configure in your `mcp.json`:

```json
{
  "mcpServers": {
    "my-sql-server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/TheJamesWilliams/j-mssql-mcp.git",
        "j-mssql-mcp"
      ],
      "env": {
        "SQL_SERVER": "your-server.example.com",
        "SQL_DATABASE": "YourDatabase",
        "SQL_PORT": "1433"
      }
    }
  }
}
```

### Option 2: From Private PyPI/Artifactory

If published to your internal package repository:

```json
{
  "mcpServers": {
    "my-sql-server": {
      "command": "uvx",
      "args": ["j-mssql-mcp"],
      "env": {
        "SQL_SERVER": "your-server.example.com",
        "SQL_DATABASE": "YourDatabase",
        "SQL_PORT": "1433"
      }
    }
  }
}
```

## Configuration

Set these environment variables in your MCP config:

- `SQL_SERVER`: SQL Server hostname (e.g., `your-server.example.com`)
- `SQL_DATABASE`: Database name (e.g., `YourDatabase`)
- `SQL_PORT`: Port number (default: `1433`)

## Usage

The server provides one tool:

### execute_sql

Execute read-only SQL queries against the configured database.

**Parameters:**

- `query` (string): The SQL SELECT statement to execute

**Example:**

```sql
SELECT TOP 10 * FROM dbo.YourTable
```

## Safety

- Only SELECT statements are allowed
- No data modification operations (INSERT, UPDATE, DELETE, etc.)
- Queries are executed with read-only intent

## Requirements

- Python 3.10+
- Windows environment (for Windows Authentication)
- ODBC Driver 18 for SQL Server (or compatible)
- Network access to SQL Server

## Development

### Local Setup

```bash
# Clone the repository
git clone https://github.com/TheJamesWilliams/j-mssql-mcp.git
cd j-mssql-mcp

# Install in development mode
pip install -e .

# Run locally
j-mssql-mcp
```

### Testing

```bash
# Set environment variables
export SQL_SERVER="your-server.example.com"
export SQL_DATABASE="YourDatabase"
export SQL_PORT="1433"

# Run the server
j-mssql-mcp
```

## Publishing

### To GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### To S3 Artifactory

```bash
# Build the package
python -m build

# Upload to S3 (configure your S3 credentials first)
aws s3 cp dist/j_mssql_mcp-1.0.0-py3-none-any.whl s3://your-bucket/python-packages/
```

## License

MIT License - Free to use and modify
