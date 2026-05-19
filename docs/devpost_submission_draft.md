# Devpost Submission Draft

### Project title

TraceLitmus

### Tagline

A reproducibility litmus test for Phoenix LLM evaluations.

### Inspiration

LLM evaluation dashboards can look clean while hiding reproducibility failures: missing baselines, prompt drift, dataset drift, and unsupported comparison claims. TraceLitmus started from a simple question: before a team trusts an eval result, can we prove the experiment is reproducible enough to compare?

### What it does

TraceLitmus connects to Phoenix through MCP, retrieves experiment artifacts, and runs deterministic reproducibility checks. It produces a Markdown reproducibility report with a score, findings, and typed evidence references. Gemini is used as an explanation layer that summarizes and prioritizes existing findings while preserving evidence IDs and scores.

### How we built it

We built TraceLitmus with Python, Streamlit, Phoenix MCP, Arize/Phoenix, a Gemini explanation layer, Cloud Run deployment files, and a deterministic report renderer. The audit core is ordinary Python: it retrieves data, normalizes objects, runs rules, computes score penalties, and renders Markdown.

### Partner technology usage

Phoenix MCP is used for the local MCP audit path. The current MCP-backed rule is `missing_baseline`. TraceLitmus retrieves Phoenix dataset and experiment records through confirmed Phoenix MCP tools, then cites the returned experiment ID in the report. Hosted MCP requires a reachable hosted Phoenix endpoint; the Cloud Run app currently defaults to offline mode until that endpoint is configured.

TraceLitmus does not claim that all rules are MCP-backed. The offline rules are demo and smoke-test coverage, while `missing_baseline` is the first real MCP-backed rule.

### Google Cloud / Gemini usage

Gemini explanation was verified locally with a rotated API key. Gemini receives a sanitized audit payload and returns an executive summary, finding explanations, and prioritized next steps. It cannot alter evidence, score, severity, or rule IDs.

Cloud Run hosts the Streamlit app in offline-default mode. Full Google Cloud Agent Builder production orchestration is not claimed in this version.

### Challenges

Phoenix MCP exposed fewer tools than initially assumed. Trace-level APIs were not available through MCP, so evidence was redesigned around MCP-addressable objects such as datasets, experiments, spans, and annotations. Cloud Run also cannot reach a local Phoenix instance on `127.0.0.1`, so hosted MCP needs Phoenix Cloud or another reachable Phoenix endpoint. Evidence safety required separating deterministic findings from Gemini prose.

### Accomplishments

TraceLitmus has a real Phoenix MCP local audit, live Gemini explanation without evidence mutation, a Cloud Run-hosted app, a structured reproducibility report, and typed evidence references. The demo package includes local reproduction commands, a hosted app, a video script, and a submission checklist.

### What we learned

MCP tool surface determines product scope. Agentic systems need deterministic evidence boundaries. Hosted demos require separating local data dependencies from deployed app behavior. Gemini is strongest here as a narrator and planner, not as the source of reproducibility judgment.

### What's next

Next steps are configuring a hosted Phoenix endpoint, adding more MCP-backed rules, wiring Cloud Run secrets for Gemini, improving the UI, and adding full Agent Builder orchestration if the final submission requirements demand it.
