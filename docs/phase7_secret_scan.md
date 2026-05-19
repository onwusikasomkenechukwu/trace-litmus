# Phase 7 Secret Scan

## Search Terms

- `AIza` [Certain]
- `GOOGLE_API_KEY` [Certain]
- `ARIZE` [Certain]
- `PHOENIX_API_KEY` [Certain]
- `BEGIN PRIVATE KEY` [Certain]
- `client_secret` [Certain]
- `service_account` [Certain]
- `credentials` [Certain]
- `.env` [Certain]
- `ak-` [Certain]

## Actual Secret Removed

An actual Google API key and a Phoenix-looking API key were found in `.env.example` during Phase 7. [Certain]

Both values were removed immediately and replaced with blank placeholders. [Certain]

The removed values are not copied into this document. [Certain]

Rotate both exposed keys before public submission. [Certain]

## Remaining Hits

- `.env.example` contains blank placeholders for `GOOGLE_API_KEY` and `PHOENIX_API_KEY`. Classification: safe placeholder. [Certain]
- `README.md` contains the placeholder `YOUR_ROTATED_KEY` in a local-only command example. Classification: safe placeholder. [Certain]
- `.gitignore`, `.dockerignore`, and setup docs mention `.env` and credential filenames. Classification: docs warning. [Certain]
- Cloud Run docs mention Secret Manager environment variable names. Classification: docs warning. [Certain]
- Arize setup docs mention placeholder names such as `<ARIZE_API_KEY>`. Classification: safe placeholder. [Certain]
- Source code reads `GOOGLE_API_KEY` and `PHOENIX_API_KEY` from environment variables. Classification: expected runtime configuration. [Certain]

## Current Status

No actual secret values remain in the repository scan after cleanup. [Certain]

This folder is not initialized as git, so no git history cleanup was possible here. [Certain]
