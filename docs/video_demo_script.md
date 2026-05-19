# TraceLitmus Demo Video Script

Target length: about 3 minutes. [Certain]

## 0:00-0:20: What TraceLitmus Is

Open the Streamlit app. [Certain]

Narration:

TraceLitmus is a reproducibility litmus test for Phoenix LLM evaluation experiments. It reads Phoenix experiment data through the Phoenix MCP server, runs deterministic audit rules, and uses Gemini only to explain the results in plain language. Gemini does not decide whether findings exist. [Certain]

## 0:20-0:45: Show The Deterministic Core

In the sidebar, select `Offline fixture`, project `demo`, leave Gemini unchecked, and run the audit. [Certain]

Point to:

- `Source: Offline fixture` [Certain]
- reproducibility score and score derivation [Certain]
- seven placeholder rule sections [Certain]
- Markdown download button [Certain]

Narration:

Offline mode is the smoke-test path. It proves the renderer, scoring, typed evidence refs, and download flow without needing Phoenix or credentials. [Certain]

## 0:45-1:35: Show Phoenix MCP Path

Switch source to `Phoenix MCP`, project `tracelitmus-demo`, leave Gemini unchecked, and run the audit. [Certain]

Point to:

- `Source: Phoenix MCP` [Certain]
- one MCP-backed rule, `missing_baseline` [Certain]
- evidence ID `experiment:RXhwZXJpbWVudDoy` [Certain]

Narration:

This is the partner integration path. TraceLitmus starts `@arizeai/phoenix-mcp`, retrieves dataset and experiment records from Phoenix through confirmed MCP tools, then runs the first real rule: missing baseline. The audit finding cites the real Phoenix experiment ID returned through MCP. [Certain]

## 1:35-2:15: Show Gemini Explanation Layer

Check `Add Gemini explanation` and rerun Phoenix MCP mode. [Certain]

Point to:

- `## Gemini Explanation` [Certain]
- executive summary [Certain]
- finding explanations [Certain]
- prioritized next steps [Certain]
- unchanged score, rule ID, severity, and evidence line [Certain]

Narration:

Gemini is the narrator, not the judge. It receives a sanitized audit payload with findings and metadata, then writes an explanation and next steps. The deterministic Python audit still owns the rule IDs, severity, score, and evidence references. [Certain]

## 2:15-2:40: Show Hosted Readiness

Open `docs/hosted_phoenix_strategy.md` or mention it. [Certain]

Narration:

For hosted demo, TraceLitmus defaults to offline mode unless a reachable Phoenix endpoint is configured. Cloud Run cannot reach a laptop Phoenix instance at `127.0.0.1`, so the preferred hosted strategy is Phoenix Cloud or another reachable Phoenix endpoint. [Certain]

## 2:40-3:00: Close

Point to README commands or the Dockerfile. [Certain]

Narration:

The repo includes a Streamlit app, Cloud Run deployment files, Docker instructions, a Gemini verifier, and a submission checklist. The current limitation is intentional: one real MCP-backed rule first, with Gemini explanation layered on top and no hidden fallbacks. [Certain]
