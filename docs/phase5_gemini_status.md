# Phase 5 Gemini Status

The old Gemini API key was exposed and must be treated as compromised. [Certain]

Use only a newly rotated key for verification. [Certain]

Do not write the key into `.env`, docs, reports, shell history exports, issue comments, commit messages, or screenshots. [Certain]

## Process-scoped verification

Run these commands from the repository root in a fresh PowerShell session. [Certain]

```powershell
$env:GOOGLE_API_KEY="NEW_ROTATED_KEY_HERE"
$env:TRACE_LITMUS_ENABLE_GEMINI="true"

python scripts\verify_gemini.py --require-live
python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp_agent.md --gemini-explanation

Remove-Item Env:\GOOGLE_API_KEY
Remove-Item Env:\TRACE_LITMUS_ENABLE_GEMINI
```

Replace `NEW_ROTATED_KEY_HERE` only in the process environment. [Certain]

Do not commit the key. [Certain]

Do not print the key. [Certain]

## Expected verification behavior

`python scripts\verify_gemini.py --require-live` should exit with status 0 and show `fallback_used: false`. [Certain]

The MCP audit command should generate `reports/demo_mcp_agent.md` with deterministic audit fields preserved and Gemini prose attached separately. [Likely]

If the live Gemini call fails, the failure must be visible. [Certain]

Do not hide a hosted demo failure behind silent fallback when the goal is live Gemini verification. [Certain]

## Current status

Live verification with the rotated key is pending manual execution by the key holder. [Certain]

This repository does not contain the old key or the new key by design. [Certain]
