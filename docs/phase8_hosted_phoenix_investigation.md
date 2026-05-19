# Phase 8 Hosted Phoenix Investigation

## Purpose

Identify the exact hosted Phoenix or Arize values TraceLitmus needs before Cloud Run MCP mode can replace the local MCP segment. [Certain]

No real API keys or space IDs are included in this document. [Certain]

## Sources Checked

- Phoenix MCP docs: `@arizeai/phoenix-mcp` accepts `npx -y @arizeai/phoenix-mcp@latest --baseUrl https://my-phoenix.com --apiKey your-api-key`. [Certain] Source: https://arize.com/docs/phoenix/sdk-api-reference/typescript/mcp-server
- Phoenix REST API docs: Phoenix Cloud base URL is `https://app.phoenix.arize.com`; self-hosted Phoenix uses its deployment URL, such as `http://localhost:6006`. [Certain] Source: https://arize.com/docs/phoenix/sdk-api-reference/rest-api/overview
- Phoenix REST API docs: authenticated calls use a bearer token header, and endpoints live under `/v1/...`. [Certain] Source: https://arize.com/docs/phoenix/sdk-api-reference/rest-api/overview
- Phoenix API key docs: Phoenix supports System API Keys, User API Keys, and Admin Secret credentials. [Certain] Source: https://arize.com/docs/phoenix/settings/api-keys
- Local setup doc: `scripts/phoenix_local_setup.md` already documents `--baseUrl` and optional `--apiKey` for the MCP package. [Certain]
- AX setup doc: `docs/arize_ax_setup.md` says TraceLitmus does not use the AX profile directly for MCP mode. [Certain]

## Values Needed For Hosted MCP

| Value | Needed Status | Notes |
| --- | --- | --- |
| `PHOENIX_BASE_URL` | Required. [Certain] | For Phoenix Cloud, the documented base URL format is `https://app.phoenix.arize.com`. [Certain] A self-hosted Phoenix deployment would use its HTTPS service URL. [Certain] |
| `PHOENIX_API_KEY` | Required if hosted Phoenix authentication is enabled. [Likely] | Phoenix Cloud requires an API key or supported token for API calls. [Likely] Store it in Secret Manager for Cloud Run. [Certain] |
| `PHOENIX_PROJECT_NAME` | Required by TraceLitmus run selection. [Certain] | Expected demo value is `tracelitmus-demo`. [Certain] |
| `PHOENIX_MCP_COMMAND` | Already known. [Certain] | `npx`. [Certain] |
| `PHOENIX_MCP_PACKAGE` | Already known. [Certain] | `@arizeai/phoenix-mcp@latest`. [Certain] |

## Hosted Arize / Phoenix Access Observed Locally

AX CLI is installed locally and has an active profile. [Certain]

AX CLI can list hosted Arize projects, but the visible project names are generic Arize demo projects, not `tracelitmus-demo`. [Certain]

The AX profile is not enough by itself to prove Phoenix MCP compatibility, because TraceLitmus MCP mode talks to Phoenix through `@arizeai/phoenix-mcp`, not through AX CLI. [Certain]

## Local Hosted Phoenix MCP Test

Test attempted with: [Certain]

- `PHOENIX_BASE_URL=https://app.phoenix.arize.com` [Certain]
- `PHOENIX_PROJECT_NAME=tracelitmus-demo` [Certain]
- API key loaded process-scoped from the local AX profile and not printed or written to disk. [Certain]

Command shape: [Certain]

```powershell
python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp_hosted.md
```

Result: failed before report creation. [Certain]

Exact non-secret error: [Certain]

```text
MCP tool list-projects returned an error:
https://app.phoenix.arize.com/v1/projects?limit=100&include_experiment_projects=true: 401 Unauthorized
```

No `reports/demo_mcp_hosted.md` file was produced. [Certain]

## `.env` Added After Initial Investigation

A local `.env` file is now present. [Certain]

The file contains secret values and must remain ignored by git. [Certain]

The configured `PHOENIX_BASE_URL` is `http://127.0.0.1:6006`, so the new `.env` supports local Phoenix MCP but does not provide a hosted Phoenix endpoint. [Certain]

With this `.env`, local Phoenix MCP still works and writes `reports\demo_mcp.md`. [Certain]

With this `.env`, live Gemini verification works locally through `python scripts\verify_gemini.py --require-live`. [Certain]

With this `.env`, MCP plus Gemini report generation works locally and writes `reports\demo_mcp_agent.md`. [Certain]

Hosted Phoenix MCP remains unverified because the `.env` still points Phoenix at localhost. [Certain]

## Second Probe After `.env` Update

The updated `.env` added `PHOENIX_COLLECTOR_ENDPOINT=https://app.arize.com`, `ARIZE_API_KEY`, and `ARIZE_SPACE_ID`. [Certain]

These values were inspected only in redacted form. [Certain]

`PHOENIX_BASE_URL` still remained `http://127.0.0.1:6006`, so TraceLitmus still defaults MCP reads to local Phoenix. [Certain]

Two process-scoped hosted probes were run without writing secrets to disk. [Certain]

| Probe | Base URL | Result | Classification |
| --- | --- | --- | --- |
| Phoenix Cloud | `https://app.phoenix.arize.com` | `401 Unauthorized` from `/v1/projects`. [Certain] | Auth failed or wrong key type. [Certain] |
| Arize app collector endpoint | `https://app.arize.com` | MCP received HTML and failed JSON parsing with `Unexpected token '<'`. [Certain] | Wrong endpoint for Phoenix MCP. [Certain] |

`PHOENIX_COLLECTOR_ENDPOINT` is not a substitute for `PHOENIX_BASE_URL` in the current TraceLitmus MCP client. [Certain]

The current client invokes `@arizeai/phoenix-mcp` with `--baseUrl` from `PHOENIX_BASE_URL`. [Certain]

## Third Probe After `PHOENIX_BASE_URL` Was Set To Phoenix Cloud

The `.env` file now sets `PHOENIX_BASE_URL=https://app.phoenix.arize.com`. [Certain]

Hosted MCP was tried again with the configured `PHOENIX_API_KEY`. [Certain]

Result: `list-projects` still returned `401 Unauthorized`. [Certain]

Hosted MCP was also tried with the configured `ARIZE_API_KEY` mapped process-scoped into `PHOENIX_API_KEY`. [Certain]

Result: `list-projects` still returned `401 Unauthorized`. [Certain]

A direct REST probe against `https://app.phoenix.arize.com/v1/projects?limit=1&include_experiment_projects=true` was run with both keys using bearer auth, `api_key` header auth, and both headers together. [Certain]

Result: every combination returned `401 Unauthorized`. [Certain]

This confirms the current credentials are not accepted by the Phoenix Cloud REST endpoint used by `@arizeai/phoenix-mcp`. [Certain]

Because `.env` now points at hosted Phoenix, the local Option B MCP command needs a process-scoped localhost override during the demo unless `.env` is switched back. [Certain]

Local fallback check with `PHOENIX_BASE_URL=http://127.0.0.1:6006` passed and wrote `reports\demo_mcp.md`. [Certain]

## Fourth Probe With `PHOENIX_TOKEN`

The `.env` file now contains `PHOENIX_TOKEN` instead of `PHOENIX_API_KEY`. [Certain]

The TraceLitmus client currently reads `PHOENIX_API_KEY`, so `PHOENIX_TOKEN` was mapped to `PHOENIX_API_KEY` process-scoped for testing only. [Certain]

Hosted MCP still failed on `list-projects` with `401 Unauthorized`. [Certain]

A direct REST probe against `/v1/projects` was also run with `PHOENIX_TOKEN` using bearer auth, `api_key`, `x-api-key`, and combined bearer plus `api_key`. [Certain]

Every direct REST auth mode returned `401 Unauthorized`. [Certain]

Conclusion: the current token is not accepted by the Phoenix Cloud `/v1/projects` endpoint used by `@arizeai/phoenix-mcp`. [Certain]

## Authentication Header Verification

TraceLitmus does not send Phoenix REST headers directly in MCP mode. [Certain]

TraceLitmus starts `@arizeai/phoenix-mcp` and passes the configured secret as the `--apiKey` argument. [Certain]

The published `@arizeai/phoenix-mcp@4.0.13` package creates a Phoenix REST client with `headers.Authorization = "Bearer " + config.apiKey`. [Certain]

The same package also sets `headers.api_key = config.apiKey` for compatibility. [Certain]

Therefore, when TraceLitmus passes a value through `--apiKey`, the MCP server does send `Authorization: Bearer {API Key}`. [Certain]

TraceLitmus now reads `PHOENIX_API_KEY` first and falls back to `PHOENIX_TOKEN` when constructing the MCP `--apiKey` argument. [Certain]

## Blocker Classification

Primary blocker: auth failed. [Certain]

Likely cause: the local AX API key is not accepted as a Phoenix Cloud API key for `https://app.phoenix.arize.com/v1/projects`, or the account needs a separate Phoenix API key. [Likely]

Current update: both the configured `PHOENIX_API_KEY` and `ARIZE_API_KEY` fail against the Phoenix Cloud `/v1/projects` endpoint. [Certain]

Latest update: the configured `PHOENIX_TOKEN` also fails against the Phoenix Cloud `/v1/projects` endpoint. [Certain]

The Arize app URL `https://app.arize.com` is not the Phoenix MCP API base URL. [Certain]

Secondary blocker: the `tracelitmus-demo` project does not appear in the hosted project list available through AX CLI. [Certain]

Not the observed blocker: network connectivity. [Certain]

The request reached the Phoenix Cloud domain and returned `401 Unauthorized`, so the failure is authentication or credential scope, not DNS or outbound network. [Certain]

## Same MCP Tools As Local

TraceLitmus uses these hosted-relevant MCP tools in the current audit path: [Certain]

- `list-projects` [Certain]
- `list-datasets` [Certain]
- `get-dataset-examples` [Certain]
- `list-experiments-for-dataset` [Certain]

The same `@arizeai/phoenix-mcp@latest` package is used locally and would be used for hosted Phoenix. [Certain]

Official MCP docs describe Phoenix MCP as a server over Phoenix capabilities and show configuration by `--baseUrl` plus `--apiKey`. [Certain]

Hosted endpoint support for the current TraceLitmus tools is not verified because authenticated `list-projects` failed. [Certain]

## Demo Data Status

Hosted `tracelitmus-demo` data is not verified. [Certain]

AX CLI did not show a `tracelitmus-demo` project in the accessible hosted Arize project list. [Certain]

The existing local seed script should not be pointed at hosted Phoenix until a correct Phoenix API key and endpoint are confirmed. [Certain]

## Manual Action Needed

Open the Arize/Phoenix dashboard, find or create the Phoenix Cloud API credential, and confirm the Phoenix endpoint URL. [Certain]

Minimum manual steps: [Certain]

1. Open Phoenix Cloud or the Arize dashboard account for the submission. [Certain]
2. Create a Phoenix System API Key or User API Key suitable for programmatic API access. [Certain]
3. Confirm the base URL is `https://app.phoenix.arize.com` or copy the account-specific hosted Phoenix URL if the dashboard provides one. [Certain]
4. Set process-scoped values locally, without writing secrets to disk. [Certain]
5. Rerun the hosted MCP audit command. [Certain]
6. If it works, seed or create `tracelitmus-demo` data, then update Cloud Run using Secret Manager for the key. [Certain]

Process-scoped shape: [Certain]

```powershell
$env:PHOENIX_BASE_URL="https://YOUR_HOSTED_PHOENIX_ENDPOINT"
$env:PHOENIX_API_KEY="HOSTED_PHOENIX_KEY_IF_REQUIRED"
$env:PHOENIX_PROJECT_NAME="tracelitmus-demo"

python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp_hosted.md

Remove-Item Env:\PHOENIX_BASE_URL
Remove-Item Env:\PHOENIX_API_KEY
Remove-Item Env:\PHOENIX_PROJECT_NAME
```

Do not put real key values, space IDs, or copied profile files in the repository. [Certain]
