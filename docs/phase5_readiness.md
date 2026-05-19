# Phase 5 Readiness

## Current Status

TraceLitmus is submission-package ready for local judging and ready for Cloud Run deployment once Docker and gcloud are available. [Likely]

The hosted MCP demo still requires a reachable hosted Phoenix endpoint. [Certain]

## Verified

- Offline CLI audit generated `reports/demo.md`. [Certain]
- Local Phoenix MCP audit generated `reports/demo_mcp.md`. [Certain]
- MCP plus live Gemini generated `reports/demo_mcp_agent.md`. [Certain]
- `scripts/verify_gemini.py --allow-fallback` succeeded with live Gemini when a process-scoped key was supplied. [Certain]
- `scripts/verify_gemini.py --require-live` succeeded with live Gemini when a process-scoped key was supplied. [Certain]
- Streamlit local UI worked at `http://127.0.0.1:8501`. [Certain]

## Blocked

Docker build and run were not tested because Docker is unavailable in the current shell. [Certain]

Exact error:

```text
docker : The term 'docker' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

Cloud Run deployment was not attempted because gcloud is unavailable in the current shell. [Certain]

Exact error:

```text
gcloud : The term 'gcloud' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

## Hosted Demo Plan

Use Phoenix Cloud as the preferred hosted Phoenix strategy. [Likely]

Set `PHOENIX_BASE_URL` to the hosted Phoenix URL and set `PHOENIX_API_KEY` through Secret Manager if needed. [Certain]

Deploy TraceLitmus to Cloud Run with `TRACE_LITMUS_DEFAULT_SOURCE=offline` until hosted Phoenix is configured. [Certain]

After hosted Phoenix is configured, switch `TRACE_LITMUS_DEFAULT_SOURCE=mcp` or leave it selectable in the UI. [Certain]

## Remaining Risk

Public rules mention Gemini and Google Cloud Agent Builder. [Likely]

TraceLitmus currently uses Gemini through the Google Gen AI SDK and prepares Cloud Run deployment, but it does not implement a full Google Cloud Agent Builder production deployment. [Certain]

Manual verification is still required before claiming Agent Builder compliance. [Certain]
