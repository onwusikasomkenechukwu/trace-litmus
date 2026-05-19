# Submission Checklist

## Required Artifacts

- Hosted project URL added to Devpost. [Pending]
- Public source repository URL added to Devpost. [Pending]
- About 3-minute demo video recorded. [Pending]
- Partner track set to Arize. [Pending]
- README includes local, Gemini, Docker, and Cloud Run instructions. [Done]
- Dockerfile exists. [Done]
- Cloud Run deployment docs exist. [Done]
- Hosted Phoenix strategy exists. [Done]

## Technical Checks

- Offline CLI audit works. [Done]
- Local Phoenix MCP CLI audit works. [Done]
- Streamlit local UI works. [Done]
- Markdown download works. [Done]
- Live Gemini verification works with a process-scoped key. [Done]
- Gemini fallback works when no key is configured. [Done]
- Docker build tested. [Blocked: Docker unavailable in this shell]
- Docker run tested. [Blocked: Docker unavailable in this shell]
- Cloud Run deploy tested. [Blocked: gcloud unavailable in this shell]
- Hosted Phoenix endpoint configured. [Pending]

## Compliance Checks

- Do not claim all seven rules are MCP-backed. [Done]
- Do not claim full Google Cloud Agent Builder production integration. [Done]
- Do not commit `.env`, service account files, API keys, or secrets. [Done]
- Keep MCP errors visible. [Done]
- Keep Gemini fallback warnings visible. [Done]
- Keep offline mode available as fallback and smoke-test path. [Done]

## Final Before Submission

- Rotate any API key pasted into chat or shell commands before public submission. [Pending]
- Configure `PHOENIX_BASE_URL` to Phoenix Cloud or another hosted Phoenix endpoint. [Pending]
- Deploy Cloud Run and test the public URL. [Pending]
- Record final video with the hosted URL and a local Phoenix MCP proof if hosted Phoenix is not ready. [Pending]
