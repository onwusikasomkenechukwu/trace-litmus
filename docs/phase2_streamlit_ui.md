# Phase 2 Streamlit UI

## Run Locally

```powershell
streamlit run streamlit_app.py
```

Open `http://127.0.0.1:8501`. [Certain]

If `streamlit` is not on PATH, run `python -m streamlit run streamlit_app.py`. [Certain]

## What It Supports

- Choose `Offline fixture` or `Phoenix MCP`. [Certain]
- Enter a project name. [Certain]
- Run the audit and render the Markdown report in the browser. [Certain]
- Download the generated Markdown report. [Certain]
- Surface MCP exceptions directly in the UI. [Certain]
- Optionally request a Gemini explanation layer. [Certain]

## Phase Boundary

Offline mode runs the seven placeholder rules against the static fixture. [Certain]

Phoenix MCP mode runs only the first real MCP-backed rule, `missing_baseline`. [Certain]

The UI does not integrate Google Cloud Agent Builder and does not deploy to Cloud Run yet. [Certain]

## Stop and Restart

Stop Streamlit by matching the entrypoint command, not a stale PID. [Certain]

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match 'python|streamlit' -and $_.CommandLine -match 'streamlit_app.py' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

Stop local Phoenix by matching the Phoenix serve command. [Certain]

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match 'python|phoenix' -and $_.CommandLine -match 'phoenix.exe.*serve|phoenix serve' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```
