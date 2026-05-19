# Phase 3 Gemini Layer

## Boundary

Gemini is a narrator and planner, not the audit judge. [Certain]

The deterministic audit pipeline still owns data retrieval, rule execution, evidence refs, severity, and score. [Certain]

Gemini receives only a sanitized payload containing project ID, source, score fields, severity counts, finding text, recommended fixes, and evidence refs. [Certain]

Gemini does not receive Phoenix API keys, Google credentials, environment variables, raw MCP transport messages, or raw Phoenix responses. [Certain]

## Output

When enabled, Gemini returns:

- executive summary [Certain]
- plain-language finding explanations [Certain]
- prioritized next steps [Certain]

The renderer places this under `## Gemini Explanation`. [Certain]

If Gemini is unavailable, the report keeps the deterministic findings and shows a warning in the same section. [Certain]

## Configuration

For Gemini API mode, set `GOOGLE_API_KEY`. [Certain]

For Vertex AI mode, set `GOOGLE_GENAI_USE_VERTEXAI=true`, `GOOGLE_CLOUD_PROJECT`, and `GOOGLE_CLOUD_LOCATION`. [Certain]

`GOOGLE_GENAI_MODEL` defaults to `gemini-2.5-flash`. [Certain]

## CLI

```powershell
python -m tracelitmus.cli audit --project demo --offline --gemini-explanation --output reports/demo.md
python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --gemini-explanation --output reports/demo_mcp.md
```

## Streamlit

Run the UI with:

```powershell
streamlit run streamlit_app.py
```

Use the `Add Gemini explanation` checkbox to request the explanation layer. [Certain]

The checkbox does not make Gemini required; failures are surfaced as warnings and the deterministic report still renders. [Certain]
