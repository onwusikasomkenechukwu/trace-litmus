# Phase 8 Provider Safety Audit

## Scope

This audit checks whether LLM provider support weakens TraceLitmus competition compliance, report honesty, or evidence safety. [Certain]

It does not add new audit rules, UI features, or hosted Phoenix probes. [Certain]

## Providers Supported

Gemini is implemented in `src/tracelitmus/agent.py`. [Certain]

Gemini was verified locally with `python scripts\verify_gemini.py --require-live`. [Certain]

Gemini is the judged LLM explanation provider for the demo. [Certain]

Anthropic integration was not found in the codebase during this pass. [Certain]

No Anthropic dependency was found in `pyproject.toml`. [Certain]

No `ANTHROPIC_API_KEY`, `TRACE_LITMUS_LLM_PROVIDER`, `anthropic`, `Anthropic`, `claude`, or `sk-ant` code path was found in `src`, `scripts`, `tests`, `docs`, `README.md`, `.env.example`, or `pyproject.toml`. [Certain]

## Provider Selection

The current CLI flag is `--gemini-explanation`. [Certain]

The current Streamlit checkbox is `Add Gemini explanation`. [Certain]

There is no selectable multi-provider LLM runtime in the current code. [Certain]

## Judged Demo Position

Gemini remains the visible explanation layer for the judged demo. [Certain]

Anthropic should not be described as a judged requirement or product power source unless actual code is added and the competition rules allow it as supporting tooling. [Certain]

README currently describes an optional Gemini explanation layer, not Anthropic-powered behavior. [Certain]

## Immutable Deterministic Fields

LLM output is explanation-only. [Certain]

Deterministic audit findings, score, severity, rule IDs, source, project ID, and evidence refs are immutable across LLM and fallback modes. [Certain]

Immutable fields: [Certain]

- `source` [Certain]
- `project_id` [Certain]
- `score` [Certain]
- `severity` [Certain]
- `rule_id` [Certain]
- evidence refs [Certain]

Implementation notes: [Certain]

- `sanitized_audit_payload()` sends a read-only summary of deterministic fields to Gemini. [Certain]
- `_prompt()` tells Gemini not to invent evidence or rewrite object IDs. [Certain]
- `attach_agent_explanation()` only sets `report.agent_explanation` or `report.agent_warning`. [Certain]
- Report rendering prints Gemini prose in a separate `## Gemini Explanation` section before deterministic findings. [Certain]

## Required Option B Verification

The local MCP path was verified with process-scoped environment overrides: [Certain]

```powershell
$env:PHOENIX_BASE_URL="http://127.0.0.1:6006"
$env:PHOENIX_PROJECT_NAME="tracelitmus-demo"

python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports\demo_mcp_agent.md --gemini-explanation

Select-String -Path reports\demo_mcp_agent.md -Pattern "Source: Phoenix MCP","Gemini Explanation","experiment:RXhwZXJpbWVudDoy","missing_baseline","94 / 100"
```

Result: command passed and wrote `reports\demo_mcp_agent.md`. [Certain]

The verification strings were present: [Certain]

- `Source: Phoenix MCP` [Certain]
- `Reproducibility score: 94 / 100` [Certain]
- `## Gemini Explanation` [Certain]
- `## missing_baseline` [Certain]
- `experiment:RXhwZXJpbWVudDoy` [Certain]

## Smoke Check Results

The offline deterministic report command passed and wrote `reports\demo.md`. [Certain]

The local Phoenix MCP report command passed with `PHOENIX_BASE_URL=http://127.0.0.1:6006` set process-scoped and wrote `reports\demo_mcp.md`. [Certain]

The local MCP plus Gemini explanation command passed with the same localhost override and wrote `reports\demo_mcp_agent.md`. [Certain]

`python scripts\verify_gemini.py --allow-fallback` passed; because a live key is currently available in `.env`, it used Gemini rather than fallback. [Certain]

`python scripts\verify_gemini.py --require-live` passed before this audit. [Certain]

`python -m py_compile src\tracelitmus\models.py src\tracelitmus\audit_rules.py src\tracelitmus\report.py src\tracelitmus\cli.py src\tracelitmus\runner.py src\tracelitmus\agent.py src\tracelitmus\web.py streamlit_app.py` passed. [Certain]

## Hosted Phoenix Status

Hosted Phoenix MCP remains blocked by `401 Unauthorized` against Phoenix Cloud. [Certain]

The published `@arizeai/phoenix-mcp@4.0.13` package sends `Authorization: Bearer {API Key}` when TraceLitmus passes a value through `--apiKey`. [Certain]

The remaining hosted blocker is credential or account-side Phoenix Cloud authorization, not TraceLitmus header formatting. [Certain]

No further hosted endpoint or header probing should be done until a confirmed Phoenix Cloud API key is provided. [Certain]

## Current Submission Path

Option B remains selected. [Certain]

The hosted app proves Cloud Run deployability in offline-default mode. [Certain]

The local Phoenix MCP segment proves partner MCP usage. [Certain]

Gemini is the judged explanation layer. [Certain]

## Secret Scan

No secret values were copied into this document. [Certain]

The final scan should ignore `.env`, which is intentionally local and ignored by git. [Certain]

The final scan ignored `.env` and found placeholders, docs warnings, code references to environment variable names, and generated warning reports only. [Certain]

Known safe hits outside `.env` include `YOUR_ROTATED_KEY`, `PHOENIX_API_KEY_IF_REQUIRED`, `NEW_ROTATED_KEY_HERE`, environment-variable names, and scan-pattern text. [Certain]

No `sk-ant` secret was found outside `.env`. [Certain]

## Compliance Risks

Do not claim hosted Phoenix MCP works until Cloud Run can reach a hosted Phoenix endpoint and run the MCP audit successfully. [Certain]

Do not claim Anthropic support unless code actually exists. [Certain]

Do not claim Gemini scoring or Gemini-generated evidence. [Certain]

Do not claim all audit rules are MCP-backed. [Certain]

## Final Recommendation

Lock Option B for the current submission package. [Certain]

Only reopen Option A after the user provides a confirmed Phoenix Cloud API key accepted by `https://app.phoenix.arize.com/v1/...`. [Certain]
