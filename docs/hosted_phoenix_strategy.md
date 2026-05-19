# Hosted Phoenix Strategy

## Problem

Cloud Run cannot reach Phoenix running on the developer laptop at `127.0.0.1:6006`. [Certain]

TraceLitmus MCP mode starts the Phoenix MCP server inside the app container, and that MCP server must reach Phoenix over the network. [Certain]

## Option A: Phoenix Cloud / Hosted Phoenix Endpoint

This is best for the final demo if Phoenix Cloud is available. [Likely]

Set `PHOENIX_BASE_URL` to the hosted endpoint. [Certain]

Set `PHOENIX_API_KEY` securely through Cloud Run secrets if the endpoint requires authentication. [Certain]

Cloud Run TraceLitmus can then reach Phoenix and run the MCP audit path. [Likely]

## Option B: Run Phoenix as a Second Cloud Run Service

This is more work. [Certain]

It requires containerizing Phoenix or using a supported Phoenix deployment path, then exposing a service URL that TraceLitmus can reach. [Certain]

TraceLitmus would set `PHOENIX_BASE_URL` to the Phoenix service URL. [Certain]

This option also needs a persistence story for seeded data. [Likely]

## Option C: Hosted App Defaults to Offline Mode, Video Shows Local MCP Mode

This is the fastest fallback. [Certain]

It is riskier for judging because partner MCP usage is less visible in the hosted project. [Likely]

Use this only as an emergency fallback. [Certain]

## Recommendation

Use Option A if Phoenix Cloud is accessible. [Likely]

Use Option B if Phoenix Cloud is not accessible and time remains. [Likely]

Use Option C only as an emergency fallback. [Certain]

## Phase 4 Decision

For now, Cloud Run deployment should default to offline mode unless a reachable Phoenix endpoint is configured. [Certain]

MCP mode remains available in the UI and should fail visibly with an actionable error if `PHOENIX_BASE_URL` is unreachable. [Certain]

## Phase 5 Decision

Do not claim hosted Phoenix MCP works until a Phoenix-compatible endpoint has been tested from the hosted environment. [Certain]

### Option A: Hosted Phoenix / Arize endpoint

Use this if the user can get a reachable Phoenix-compatible endpoint from Arize. [Likely]

Required:

- hosted `PHOENIX_BASE_URL` [Certain]
- API key configured locally or through Cloud Run secrets, if the endpoint requires authentication [Certain]
- seeded `tracelitmus-demo` project [Certain]
- MCP mode works from Cloud Run or another hosted environment [Certain]

Do not claim Option A unless tested. [Certain]

### Option B: Hosted app offline-default, local MCP video

Use this if Cloud Run works but hosted Phoenix is not ready. [Likely]

Required:

- hosted app runs offline mode [Certain]
- local video demonstrates Phoenix MCP path [Certain]
- README explains local reproduction [Certain]
- no claim that hosted MCP works [Certain]

This is the honest fallback if the hosted Phoenix endpoint remains unresolved. [Certain]

### Option C: Local-only submission

Use this only if Cloud Run cannot be deployed. [Certain]

Required:

- offline CLI audit works locally [Certain]
- local Streamlit UI works [Certain]
- local Phoenix MCP audit works, if Phoenix and `npx` are available [Likely]
- README and demo script explain that deployment tooling remained blocked [Certain]

## Phase 5 Recommendation

Prefer Option A if hosted Phoenix is reachable quickly. [Likely]

Use Option B if Cloud Run works but hosted Phoenix remains unresolved. [Likely]

Use Option C only if deployment tooling remains blocked. [Certain]
