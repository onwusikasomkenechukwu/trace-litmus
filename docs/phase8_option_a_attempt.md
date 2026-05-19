# Phase 8 Option A Attempt

## Goal

Try to upgrade the submission path from Option B to Option A without breaking the safe fallback. [Certain]

Option A target: Cloud Run TraceLitmus hosted app to hosted Phoenix endpoint to Phoenix MCP audit to Gemini explanation. [Certain]

## Safe Fallback Baseline

These checks were run on 2026-05-19 from `C:\Users\onwus\Downloads\gemini-agents-2026`. [Certain]

| Check | Result |
| --- | --- |
| `python -m tracelitmus.cli audit --project demo --offline --output reports\demo.md` | Passed and wrote `reports\demo.md`. [Certain] |
| `python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports\demo_mcp.md` | Passed and wrote `reports\demo_mcp.md`. [Certain] |
| `python scripts\verify_gemini.py --allow-fallback` | Passed with Gemini fallback because `GOOGLE_API_KEY` was not set. [Certain] |
| `gcloud run services describe tracelitmus --region us-central1 --format="value(status.url)"` | Blocked because `gcloud` is not installed or not on PATH in this shell. [Certain] |

## Hosted App Reachability

`Invoke-WebRequest` to `https://tracelitmus-vemlexqp2q-uc.a.run.app` returned HTTP 200 and a Streamlit response body. [Certain]

This confirms the hosted app endpoint is reachable from this environment. [Certain]

It does not confirm hosted Phoenix MCP, because hosted Phoenix is still not configured. [Certain]

## Hosted Phoenix Configuration Check

No process-level `PHOENIX_BASE_URL` was set in this shell. [Certain]

No local `.env` file was present. [Certain]

`.env.example` still points `PHOENIX_BASE_URL` at `http://127.0.0.1:6006`, which is only suitable for local Phoenix, not Cloud Run. [Certain]

## Option A Status

Option A is not verified. [Certain]

The blocker is specific: no reachable hosted Phoenix endpoint has been provided or configured, and this shell cannot inspect or update Cloud Run settings because `gcloud` is unavailable. [Certain]

## Required Next Step To Test Option A

Provide or configure a hosted Phoenix endpoint reachable from Cloud Run. [Certain]

Set Cloud Run environment variables without committing secrets: [Certain]

```powershell
gcloud run services update tracelitmus `
  --region us-central1 `
  --set-env-vars PHOENIX_BASE_URL=https://YOUR_HOSTED_PHOENIX_ENDPOINT,PHOENIX_PROJECT_NAME=tracelitmus-demo,TRACE_LITMUS_DEFAULT_SOURCE=mcp
```

If hosted Phoenix requires an API key, store it in Secret Manager and bind it to `PHOENIX_API_KEY` instead of putting it in source files or command history. [Certain]

After updating Cloud Run, use the hosted UI to select Phoenix MCP, run the audit, and confirm the report says `Source: Phoenix MCP` with real hosted Phoenix evidence. [Certain]

Do not claim Option A until that hosted UI test passes. [Certain]

## Fallback Status

Option B remains clean and ready: hosted app in offline-default mode, local Phoenix MCP proof in the video, and Gemini fallback when credentials are absent. [Certain]

