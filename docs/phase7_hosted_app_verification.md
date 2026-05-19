# Phase 7 Hosted App Verification

## Hosted URL

https://tracelitmus-vemlexqp2q-uc.a.run.app [Certain]

## Check Time

Checked from this environment on 2026-05-19 at about 03:04 EDT. [Certain]

## Results

- App loads in browser. [Certain]
- Hosted app defaults to `Offline fixture`. [Certain]
- Offline mode runs successfully. [Certain]
- Report renders in browser. [Certain]
- Markdown download button is visible after running offline mode. [Certain]
- Gemini is disabled in the hosted environment by default. [Certain]
- Phoenix MCP mode is not configured for hosted Phoenix. [Certain]
- When Phoenix MCP is selected, the app shows: `Cloud Run cannot reach a Phoenix instance on 127.0.0.1. Configure a hosted PHOENIX_BASE_URL.` [Certain]
- Running hosted Phoenix MCP fails visibly, not silently. [Certain]

## Exact Hosted MCP Error

```text
PhoenixMCPError: MCP tool list-projects returned an error: meta=None content=[TextContent(type='text', text='fetch failed', annotations=None, meta=None)] structuredContent=None isError=True
```

## Interpretation

The hosted app is valid as an offline-default Cloud Run demo. [Certain]

The hosted app does not prove hosted Phoenix MCP until `PHOENIX_BASE_URL` points to a reachable hosted Phoenix endpoint. [Certain]

The local Phoenix MCP path remains the verified partner MCP demo path. [Certain]
