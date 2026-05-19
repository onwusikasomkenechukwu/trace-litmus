# TraceLitmus Architecture

## Phoenix MCP client layer

`PhoenixMCPClient` supports offline fixture mode and a real stdio MCP mode for confirmed Phoenix MCP tools. [Certain]

- Prompt access uses `list-prompts`, `get-latest-prompt`, `get-prompt-by-identifier`, `get-prompt-version`, `list-prompt-versions`, `get-prompt-version-by-tag`, `list-prompt-version-tags`, `add-prompt-version-tag`, and `upsert-prompt`. [Certain]
- Project discovery uses `list-projects`. [Certain]
- Span evidence uses `get-spans` and `get-span-annotations`. [Certain]
- Dataset evidence uses `list-datasets`, `get-dataset-examples`, `get-dataset-experiments`, and `add-dataset-examples`. [Certain]
- Experiment evidence uses `list-experiments-for-dataset` and `get-experiment-by-id`. [Certain]
- The architecture excludes every unconfirmed tool name from the client layer. [Certain]

Phase 1 reads datasets and experiments through `@arizeai/phoenix-mcp`, then runs only `detect_missing_baseline` for the live MCP report. [Certain]

## Audit rule engine

The rule engine is deterministic Python code that consumes normalized Phoenix objects. [Certain]

- `detect_missing_seed` reads experiment metadata and metrics. [Certain]
- `detect_prompt_drift` compares experiment prompt version IDs against prompt version records. [Certain]
- `detect_dataset_drift` compares experiment dataset IDs against dataset records. [Certain]
- `detect_missing_baseline` reads experiment metadata and baseline links. [Certain]
- `detect_metric_ambiguity` reads metric names, definitions, directions, and evaluator metadata. [Likely]
- `detect_no_statistical_support` reads confidence intervals, variance estimates, and sample metadata. [Likely]
- `detect_weak_sample_size` reads experiment sample sizes and dataset example counts. [Certain]

## Gemini/Agent Builder orchestration boundary

Gemini decides how to explain findings, rank narrative emphasis, and suggest concise remediation language. [Likely]

Python code decides which Phoenix MCP calls run, how objects are normalized, which audit rules fire, how scores are computed, and which Phoenix object IDs are cited. [Certain]

LLM output cannot create evidence, mutate rule results, or remove Phoenix IDs from report findings. [Certain]

Phase 3 implements this as an optional Gemini explanation layer through the Google Gen AI SDK, with Vertex AI configuration supported through environment variables. [Certain]

This is not a deployed Google Cloud Agent Builder or Agent Engine integration yet. [Certain]

## Report renderer

Markdown is the primary artifact because it is easy to diff, inspect, and submit with a demo. [Certain]

HTML is secondary and should be rendered from the same `AuditReport` object after Markdown works. [Certain]

The Phase 0 renderer uses `templates/report.md.j2` and keeps one section per audit rule. [Certain]

## Demo Phoenix fixture setup

Phase 1 should describe a local Phoenix Docker setup plus a Python seeder script under `scripts/`. [Certain]

The seeder should create one demo project, two prompt versions, two dataset versions, three experiments, and span-level evidence that reproduces the offline fixture shape. [Likely]

The fixture is only for skeleton testing; the real integration path must call confirmed Phoenix MCP tools. [Certain]

## Web UI layer

The web framework is still TBD. [Certain]

The likely choices are FastAPI with minimal HTML or Next.js with a small API layer. [Guessing]

The first hosted demo should show project selection, audit progress, score, seven rule sections, and cited Phoenix object IDs. [Likely]
