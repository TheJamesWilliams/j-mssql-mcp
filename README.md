# j-mssql-mcp

SQL Server MCP Server with Windows Authentication support for Kiro AI.

## Features

- Windows Authentication / Kerberos (Trusted Connection) for SQL Server
- Works on Windows, Mac, and Linux
- Environment-based configuration
- Read-only query execution for safety
- No passwords in configuration files

## Installation

### Option 1: From PyPI with uvx (Recommended)

No installation needed! Just configure in your `mcp.json`:

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

### Option 2: Direct from GitHub with uvx

**Prerequisites:** Git must be installed on your system.

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

### Option 3: Install via pip

If you don't have Git installed, you can install directly via pip:

```bash
pip install j-mssql-mcp
```

Then use in your `mcp.json`:

```json
{
  "mcpServers": {
    "my-sql-server": {
      "command": "j-mssql-mcp",
      "args": [],
      "env": {
        "SQL_SERVER": "your-server.example.com",
        "SQL_DATABASE": "YourDatabase",
        "SQL_PORT": "1433"
      }
    }
  }
}
```

### Option 4: From Private PyPI/Artifactory

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

## Troubleshooting

### "Git executable not found" Error

**Problem:** `uvx` needs Git to install from GitHub.

**Check if Git is installed:**

```bash
git --version
```

**If Git is installed but still getting the error (Windows):**

Git is installed but not in the system PATH. Fix it:

1. Find Git location:

   ```powershell
   where git
   # Usually: C:\Program Files\Git\cmd\git.exe
   ```

2. Add to System PATH:
   - Press `Win + X` → System → Advanced system settings
   - Environment Variables → System variables → Path → Edit
   - Add: `C:\Program Files\Git\cmd`
   - Click OK on all dialogs
   - **Restart Kiro/your terminal**

**Alternative: Use pip installation instead** (see Option 2 in Installation section above)

**If Git is not installed:**

- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win) or `winget install Git.Git`
- **Mac**: `brew install git` or install Xcode Command Line Tools
- **Linux**: `sudo apt install git` or `sudo yum install git`

### "Can't open lib 'ODBC Driver 18 for SQL Server'"

Install the ODBC driver:

- **Mac**: `brew install msodbcsql18`
- **Windows**: Download from [Microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- **Linux**: Follow [Microsoft's instructions](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)

### "Login failed" or Authentication Errors

**Mac/Linux users**: Run `kinit your-username@YOUR-DOMAIN.COM` to get Kerberos tickets

**Windows users**: Ensure your machine is domain-joined and you're logged in with domain credentials

### Check Your Kerberos Tickets (Mac/Linux)

```bash
klist
# Look for a ticket like: MSSQLSvc/your-server.domain.com:1433@DOMAIN.COM
```

## Requirements

- Python 3.10+
- ODBC Driver 18 for SQL Server (or compatible)
- Network access to SQL Server
- Domain-joined machine OR Kerberos authentication configured
- **Git** (required for installation from GitHub)

## Prerequisites by Platform

### Windows Users

If your machine is joined to the domain, you're all set! Windows Authentication will work automatically using your logged-in credentials.

### Mac/Linux Users

You need to authenticate with Kerberos before using the MCP:

```bash
# Authenticate with your domain credentials
kinit your-username@YOUR-DOMAIN.COM

# Verify you have tickets
klist

# You should see tickets including one for MSSQLSvc
```

**Note:** Kerberos tickets typically expire after 8-10 hours. If the MCP stops working, run `kinit` again to refresh your tickets.

**Tip:** If you already use Azure Data Studio or other domain-authenticated tools, you likely already have valid tickets!

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
