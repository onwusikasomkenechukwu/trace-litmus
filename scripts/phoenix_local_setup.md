# Local Phoenix and MCP Setup

## 1. Create a Python Virtual Environment

```powershell
cd C:\Users\onwus\Downloads\gemini-agents-2026
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## 2. Install Phoenix Dependencies

```powershell
python -m pip install arize-phoenix arize-phoenix-client
python -m pip install -e .
```

The TraceLitmus seeder uses Phoenix REST endpoints, so the client package is mainly useful for manual inspection and future scripts. [Certain]

The editable install provides TraceLitmus dependencies, including the Python `mcp` client used to call `@arizeai/phoenix-mcp`. [Certain]

## 3. Run Phoenix Locally

In a separate terminal:

```powershell
phoenix serve
```

If the installed Phoenix command differs, use the local Phoenix package instructions for starting the server. [Likely]

## 4. Confirm Phoenix Is Reachable

```powershell
Invoke-WebRequest http://127.0.0.1:6006 -UseBasicParsing
```

A successful HTTP response means the local Phoenix UI is reachable. [Certain]

## 5. Configure Environment Variables

Create `.env` from `.env.example` and fill only the values you need. [Certain]

```powershell
Copy-Item .env.example .env
```

Local Phoenix normally does not require `PHOENIX_API_KEY`. [Likely]

Use placeholders for hosted credentials until you have real credentials. [Certain]

```env
PHOENIX_BASE_URL=http://127.0.0.1:6006
PHOENIX_API_KEY=
PHOENIX_PROJECT_NAME=tracelitmus-demo
PHOENIX_DATASET_NAME=tracelitmus-demo-dataset
PHOENIX_MCP_COMMAND=npx
PHOENIX_MCP_PACKAGE=@arizeai/phoenix-mcp@latest
```

## 6. Seed Demo Data

```powershell
python scripts\seed_demo_phoenix.py
```

This writes the dataset and experiments into Phoenix. [Certain]

## 7. Install or Run Phoenix MCP

You can let `npx` fetch the MCP package on demand:

```powershell
npx -y @arizeai/phoenix-mcp@latest --baseUrl http://127.0.0.1:6006
```

For hosted Phoenix, include an API key:

```powershell
npx -y @arizeai/phoenix-mcp@latest --baseUrl https://YOUR-PHOENIX-HOST --apiKey YOUR-PHOENIX-API-KEY
```

The current package supports `--baseUrl` and optional `--apiKey` arguments. [Certain]

## 8. Run the TraceLitmus MCP Audit

```powershell
python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp.md
```

This command reads through Phoenix MCP, not the offline fixture. [Certain]

## 9. Run the Streamlit Demo UI

```powershell
streamlit run streamlit_app.py
```

If `streamlit` is not on PATH, use:

```powershell
python -m streamlit run streamlit_app.py
```

## 10. Stop or Restart Local Services

Stop Streamlit:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match 'python|streamlit' -and $_.CommandLine -match 'streamlit_app.py' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

Stop Phoenix:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match 'python|phoenix' -and $_.CommandLine -match 'phoenix.exe.*serve|phoenix serve' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

Restart by rerunning `phoenix serve` and then `streamlit run streamlit_app.py`. [Certain]
