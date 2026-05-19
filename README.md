# TraceLitmus

## Hosted demo

Hosted URL:

[https://tracelitmus-vemlexqp2q-uc.a.run.app](https://tracelitmus-vemlexqp2q-uc.a.run.app)

The hosted app currently defaults to offline demo mode. [Certain]

Phoenix MCP mode is implemented and verified locally. [Certain]

Hosted Phoenix MCP requires a reachable hosted Phoenix endpoint, because Cloud Run cannot reach Phoenix on a developer laptop at `127.0.0.1:6006`. [Certain]

Use the local Phoenix MCP demo below to reproduce the partner MCP path. [Certain]

## What this is

TraceLitmus is a reproducibility litmus test for Phoenix LLM evaluation experiments with an optional Gemini explanation layer. [Certain]

This repo contains a local and container-ready TraceLitmus demo for the Google Cloud Rapid Agent Hackathon, Arize/Phoenix partner track. [Certain]

## How it runs

```bash
python -m tracelitmus.cli audit --project demo --offline --output reports/demo.md
```

The offline command reads `tests/fixtures/sample_phoenix_response.json`, runs placeholder audit rules, and writes a Markdown report. [Certain]

Run the local web UI with:

```powershell
streamlit run streamlit_app.py
```

The UI supports both the offline fixture and the live Phoenix MCP audit path. [Certain]

If `streamlit` is not on PATH, use:

```powershell
python -m streamlit run streamlit_app.py
```

Stop Streamlit cleanly:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match 'python|streamlit' -and $_.CommandLine -match 'streamlit_app.py' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

Stop local Phoenix cleanly:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match 'python|phoenix' -and $_.CommandLine -match 'phoenix.exe.*serve|phoenix serve' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

## Local Phoenix MCP demo

```powershell
# Terminal 1: start Phoenix if not already running
# Follow scripts/phoenix_local_setup.md

# Terminal 2: seed or verify demo data
python scripts\seed_demo_phoenix.py

# Run MCP audit
$env:PHOENIX_BASE_URL="http://127.0.0.1:6006"
$env:PHOENIX_PROJECT_NAME="tracelitmus-demo"

python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp.md

Remove-Item Env:\PHOENIX_BASE_URL
Remove-Item Env:\PHOENIX_PROJECT_NAME

# Run MCP + Gemini explanation, only after setting a rotated key process-scoped
$env:PHOENIX_BASE_URL="http://127.0.0.1:6006"
$env:PHOENIX_PROJECT_NAME="tracelitmus-demo"
$env:GOOGLE_API_KEY="YOUR_ROTATED_KEY"
$env:TRACE_LITMUS_ENABLE_GEMINI="true"

python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp_agent.md --gemini-explanation

Remove-Item Env:\PHOENIX_BASE_URL
Remove-Item Env:\PHOENIX_PROJECT_NAME
Remove-Item Env:\GOOGLE_API_KEY
Remove-Item Env:\TRACE_LITMUS_ENABLE_GEMINI
```

The MCP commands require a reachable Phoenix instance and `@arizeai/phoenix-mcp` through `npx`. [Certain]

## What is deterministic vs Gemini-generated

Deterministic Python rules produce audit findings. [Certain]

Deterministic Python code computes the reproducibility score. [Certain]

Deterministic Python code preserves evidence references. [Certain]

Gemini only explains and prioritizes existing findings. [Certain]

Gemini cannot alter evidence, score, severity, or rule IDs. [Certain]

## Demo path link

See [docs/demo_path.md](docs/demo_path.md). [Certain]

## Deployment and verification

Run the local app:

```powershell
streamlit run streamlit_app.py
```

Verify Gemini behavior:

```powershell
python scripts\verify_gemini.py --allow-fallback
python scripts\verify_gemini.py --require-live
```

Build and run the Docker image:

```powershell
docker build -t tracelitmus .
docker run --rm -p 8080:8080 --env-file .env tracelitmus
```

See [docs/cloud_run_deploy.md](docs/cloud_run_deploy.md) for Cloud Run deployment. [Certain]

Cloud Run cannot reach Phoenix at `127.0.0.1`; configure a hosted `PHOENIX_BASE_URL` for MCP mode. [Certain]

## Current limitations

- One MCP-backed rule is implemented: `missing_baseline`. [Certain]
- Hosted Phoenix is not configured. [Certain]
- The hosted app defaults to offline mode as a fallback and demo path. [Certain]
- Full Google Cloud Agent Builder production orchestration is not implemented. [Certain]
- Offline mode is not the primary partner integration. [Certain]

## Phase 5 Judge Verification

Run the core smoke checks:

```powershell
python -m tracelitmus.cli audit --project demo --offline --output reports/demo.md

$env:PHOENIX_BASE_URL="http://127.0.0.1:6006"
$env:PHOENIX_PROJECT_NAME="tracelitmus-demo"

python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp.md
python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp_agent.md --gemini-explanation

Remove-Item Env:\PHOENIX_BASE_URL
Remove-Item Env:\PHOENIX_PROJECT_NAME
```

Verify Gemini:

```powershell
python scripts\verify_gemini.py --allow-fallback
python scripts\verify_gemini.py --require-live
```

`--allow-fallback` should always produce a deterministic result, even without Gemini credentials. [Certain]

`--require-live` requires a valid `GOOGLE_API_KEY` or configured Vertex AI credentials. [Certain]

Submission docs:

- [docs/video_demo_script.md](docs/video_demo_script.md) [Certain]
- [docs/submission_checklist.md](docs/submission_checklist.md) [Certain]
- [docs/phase5_readiness.md](docs/phase5_readiness.md) [Certain]
- [docs/hosted_phoenix_strategy.md](docs/hosted_phoenix_strategy.md) [Certain]
- [docs/arize_ax_setup.md](docs/arize_ax_setup.md) [Certain]
- [docs/phase5_gemini_status.md](docs/phase5_gemini_status.md) [Certain]

Important hosted-demo warning: Cloud Run cannot reach local Phoenix at `127.0.0.1:6006`; configure Phoenix Cloud or another hosted Phoenix endpoint for judge-facing MCP mode. [Certain]

## License

MIT. [Certain]
