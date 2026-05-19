# Phase 8 Final Report

## Safe Option B Baseline

Option B remains intact. [Certain]

| Check | Status |
| --- | --- |
| Offline CLI audit | Passed and wrote `reports\demo.md`. [Certain] |
| Local Phoenix MCP audit | Passed and wrote `reports\demo_mcp.md`. [Certain] |
| Gemini fallback | Passed with `python scripts\verify_gemini.py --allow-fallback`. [Certain] |
| Live Gemini local verification | Passed with `python scripts\verify_gemini.py --require-live` after `.env` was added. [Certain] |
| Local MCP plus Gemini report | Passed and wrote `reports\demo_mcp_agent.md`. [Certain] |
| Hosted app reachability | Cloud Run URL returned HTTP 200 and a Streamlit response body. [Certain] |
| Cloud Run describe | Blocked because `gcloud` is unavailable in this shell. [Certain] |

## Hosted Phoenix Investigation Result

The documented Phoenix Cloud base URL is `https://app.phoenix.arize.com`. [Certain]

The MCP package accepts `--baseUrl` and optional `--apiKey`. [Certain]

Local AX CLI access exists, but the AX profile credential did not authenticate against Phoenix Cloud MCP/REST. [Certain]

Hosted `tracelitmus-demo` data is not verified. [Certain]

## Hosted MCP Status

Hosted MCP is not working yet. [Certain]

The local hosted test reached Phoenix Cloud and failed on `list-projects` with `401 Unauthorized`. [Certain]

Classification: auth failed or wrong credential type for Phoenix Cloud. [Certain]

No hosted MCP report was created. [Certain]

The `.env` file is now configured with `PHOENIX_BASE_URL=https://app.phoenix.arize.com`. [Certain]

The hosted MCP test still fails with `401 Unauthorized`. [Certain]

Both the configured `PHOENIX_API_KEY` and `ARIZE_API_KEY` were tested against Phoenix Cloud without printing secrets, and both were rejected. [Certain]

The configured `PHOENIX_TOKEN` was also mapped process-scoped into `PHOENIX_API_KEY` and tested through MCP; it was rejected with `401 Unauthorized`. [Certain]

Direct REST probes with `PHOENIX_TOKEN` using bearer, `api_key`, `x-api-key`, and combined headers also returned `401 Unauthorized`. [Certain]

Authentication header format was verified against the published `@arizeai/phoenix-mcp@4.0.13` package. [Certain]

The MCP server sends `Authorization: Bearer {API Key}` when TraceLitmus passes the secret through `--apiKey`. [Certain]

TraceLitmus now supports `PHOENIX_TOKEN` as a fallback source for that `--apiKey` value. [Certain]

A second probe after the `.env` update confirmed that `https://app.arize.com` is not a Phoenix MCP API base URL, because MCP received HTML instead of JSON. [Certain]

`PHOENIX_COLLECTOR_ENDPOINT` does not change the current MCP read path. [Certain]

## Hosted Gemini Status

Hosted Gemini was not tested in Phase 8 because hosted MCP did not work. [Certain]

Gemini fallback remains verified locally. [Certain]

Live Gemini works locally through the existing agent boundary with the new `.env`. [Certain]

## Cloud Run Env Status

No Cloud Run environment changes were made. [Certain]

Reason: local hosted Phoenix MCP did not pass, and `gcloud` is unavailable in this shell. [Certain]

Do not set `TRACE_LITMUS_DEFAULT_SOURCE=mcp` in Cloud Run until hosted Phoenix MCP succeeds locally. [Certain]

## Option A Status

Option A did not succeed in Phase 8. [Certain]

The blocker is exact: `https://app.phoenix.arize.com/v1/projects?...` returned `401 Unauthorized` when called through `@arizeai/phoenix-mcp` with the available local AX credential. [Certain]

The latest `.env` points at Phoenix Cloud, but the credentials are still rejected by Phoenix Cloud. [Certain]

The added Arize collector endpoint also does not change Option A status because it is not accepted as a Phoenix MCP API base. [Certain]

## Option B Status

Option B remains selected. [Certain]

The final video should show the hosted Cloud Run app in offline mode, then switch to local Phoenix MCP for the partner integration proof. [Certain]

With the current `.env`, local MCP needs a process-scoped override: `PHOENIX_BASE_URL=http://127.0.0.1:6006`. [Certain]

## Extra MCP-backed Rule

No extra MCP-backed rule was added. [Certain]

Reason: deployment stability was not upgraded to Option A, so adding audit surface would be the wrong risk. [Certain]

## Exact Remaining Blockers

- Need a Phoenix Cloud API key or hosted Phoenix credential accepted by `https://app.phoenix.arize.com/v1/...`. [Certain]
- `PHOENIX_TOKEN` as currently configured is not accepted by that endpoint. [Certain]
- Need `PHOENIX_BASE_URL` set to a Phoenix API endpoint, not an Arize app or collector URL. [Certain]
- Need a hosted `tracelitmus-demo` project, dataset, examples, and experiments. [Certain]
- Need Cloud Run env update through `gcloud` or the Google Cloud console after local hosted MCP passes. [Certain]
- Need Secret Manager binding for `PHOENIX_API_KEY` before public hosted MCP demo. [Certain]

## Recommendation For Next Phase

Do one manual credential pass, not more code. [Certain]

Open Phoenix Cloud, create the correct Phoenix API key, rerun the local hosted MCP test, then decide: [Certain]

- If local hosted MCP passes, seed hosted demo data and update Cloud Run with Secret Manager. [Certain]
- If it still fails, keep Option B and submit with the current honest demo script. [Certain]
