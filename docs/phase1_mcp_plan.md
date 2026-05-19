# Phase 1 MCP Plan

## Local Phoenix Setup Plan

Run Phoenix locally at `http://localhost:6006`. [Certain]

The setup path is documented in `scripts/phoenix_local_setup.md`. [Certain]

The local Phoenix instance must be reachable before seeding or MCP audit commands run. [Certain]

## Phoenix MCP Connection Plan

TraceLitmus starts `@arizeai/phoenix-mcp` over stdio with `npx -y @arizeai/phoenix-mcp@latest --baseUrl <PHOENIX_BASE_URL>`. [Certain]

If `PHOENIX_API_KEY` is set, TraceLitmus also passes `--apiKey <PHOENIX_API_KEY>`. [Certain]

The MCP client uses the Python `mcp` package to speak JSON-RPC over stdio and calls only confirmed tool names. [Certain]

No MCP call silently falls back to the offline fixture. [Certain]

## Seed-Data Plan

Use `scripts/seed_demo_phoenix.py` to write demo data into Phoenix through REST endpoints. [Certain]

The seeder creates or appends to dataset `PHOENIX_DATASET_NAME`, defaulting to `tracelitmus-demo-dataset`. [Certain]

The seeder creates one baseline experiment and one candidate experiment whose metadata intentionally omits `baseline_experiment_id`. [Certain]

The Python seeder is setup-only; the TraceLitmus audit path reads the seeded objects through Phoenix MCP. [Certain]

## MCP Tools Phase 1 Will Call

- `list-projects`, to verify the Phoenix project surface is reachable. [Certain]
- `list-datasets`, to find the seeded dataset. [Certain]
- `get-dataset-examples`, to retrieve example count for fallback evidence. [Certain]
- `list-experiments-for-dataset`, to retrieve experiment metadata for the real rule. [Certain]

TraceLitmus will not call unconfirmed Phoenix MCP tools in Phase 1. [Certain]

## First Rule

The first real MCP-backed rule is `detect_missing_baseline`. [Certain]

It flags a non-baseline experiment that lacks `baseline_experiment_id`, `baseline_experiment`, or `reference_experiment_id` in metadata and metrics. [Certain]

The report evidence cites the Phoenix experiment ID returned through MCP. [Certain]

## Fallback Rule

If no experiments are returned through MCP, the fallback is `weak_sample_size`. [Certain]

The fallback uses `get-dataset-examples` and cites the real dataset ID plus dataset example IDs when Phoenix returns them. [Certain]

## Acceptance Command

```powershell
python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp.md
```

Expected output: `reports/demo_mcp.md` containing one MCP-backed finding and at least one Phoenix object ID returned by MCP. [Certain]

## Known Risks

Phoenix local startup and package install are outside the TraceLitmus code path, so environment setup can fail before the MCP audit runs. [Certain]

Phoenix experiment creation can differ across Phoenix versions; the seeder uses documented REST endpoints for dataset upload and experiment creation. [Likely]

If Phoenix returns experiment metadata without user-supplied fields, `missing_baseline` may need to shift to the fallback `weak_sample_size`. [Likely]

`npx` must be available on PATH, or `PHOENIX_MCP_COMMAND` must point to a working executable. [Certain]

The project dependency list includes `mcp>=1.24` for the stdio client wrapper. [Certain]
