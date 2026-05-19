# Cloud Run Deployment

## Build Locally

```powershell
docker build -t tracelitmus .
```

## Run Locally

```powershell
docker run --rm -p 8080:8080 --env-file .env tracelitmus
```

Open `http://127.0.0.1:8080`. [Certain]

If you do not have a `.env` file, create one from `.env.example` and leave secrets blank. [Certain]

## Deploy to Cloud Run

```powershell
gcloud run deploy tracelitmus `
  --source . `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars TRACE_LITMUS_DEFAULT_SOURCE=offline,TRACE_LITMUS_ENABLE_GEMINI=false
```

Do not put API keys directly in `--set-env-vars`. [Certain]

## Required Environment Variables

- `TRACE_LITMUS_DEFAULT_SOURCE`, usually `offline` until Phoenix is hosted. [Certain]
- `TRACE_LITMUS_DEFAULT_PROJECT`, default `demo`. [Certain]
- `TRACE_LITMUS_REPORT_DIR`, default `reports`. [Certain]
- `TRACE_LITMUS_ENABLE_GEMINI`, default `false`. [Certain]
- `GOOGLE_GENAI_MODEL`, default `gemini-2.5-flash`. [Certain]
- `PHOENIX_BASE_URL`, required for MCP mode. [Certain]
- `PHOENIX_API_KEY`, required only when the Phoenix endpoint requires it. [Likely]

## Hosted Phoenix Warning

`PHOENIX_BASE_URL=http://127.0.0.1:6006` will not work from Cloud Run because it points back at the Cloud Run container, not the developer laptop. [Certain]

For hosted MCP mode, set `PHOENIX_BASE_URL` to Phoenix Cloud or another reachable HTTPS endpoint. [Certain]

## Secrets

Store `GOOGLE_API_KEY` and `PHOENIX_API_KEY` in Secret Manager, then mount them as Cloud Run environment variables. [Certain]

Example shape:

```powershell
gcloud secrets create tracelitmus-google-api-key --data-file=google_api_key.txt
gcloud run services update tracelitmus `
  --region us-central1 `
  --set-secrets GOOGLE_API_KEY=tracelitmus-google-api-key:latest
```

Use the same pattern for `PHOENIX_API_KEY` if hosted Phoenix requires a key. [Certain]

## Test the Deployed URL

1. Open the Cloud Run service URL. [Certain]
2. Run offline mode first. [Certain]
3. Confirm the report renders and downloads. [Certain]
4. Switch to Phoenix MCP only after `PHOENIX_BASE_URL` points at a reachable hosted Phoenix endpoint. [Certain]
5. If Gemini is enabled without credentials, confirm the visible fallback warning appears. [Certain]

## Local Phase 5 Blocker

Cloud Run deployment was not attempted in the current shell because `gcloud` is unavailable. [Certain]

Exact error:

```text
gcloud : The term 'gcloud' is not recognized as the name of a cmdlet, function, script file, or operable program.
```
