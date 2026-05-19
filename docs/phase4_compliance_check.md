# Phase 4 Compliance Check

## Local Rules Check

Official rules not present in repository; manual verification required before submission. [Certain]

The local README identifies the project as a Google Cloud Rapid Agent Hackathon, Arize/Phoenix partner track project, but it is not an official rules document. [Certain]

## Public Sources Checked

- Devpost rules page: `https://rapid-agent.devpost.com/rules`. [Certain]
- Devpost Arize resources page: `https://rapid-agent.devpost.com/details/arize-resources`. [Certain]
- Devpost overview/update page: `https://rapid-agent.devpost.com/updates/43941-the-challenge-is-live-meet-your-partners`. [Certain]

## What Submission Requires For Google Cloud Usage

The public Devpost rules describe the project as a functional agent powered by Gemini and Google Cloud Agent Builder that integrates a partner MCP server. [Likely]

The rules also say projects should use Google Cloud and the partner products relevant to the selected track. [Likely]

The Arize resource page says the Arize track requires a code-owned agent runtime, with examples including Gemini CLI, Gemini Enterprise Agent Platform SDK, Google ADK, Agent Runtime, or Cloud Run. [Likely]

## Is Direct Gemini API Usage Enough

Direct Gemini API usage alone is probably not enough for the full submission language because the public rules mention Google Cloud Agent Builder. [Likely]

For this codebase, direct Gemini currently provides the explanation layer, while Cloud Run deployment files provide a Google Cloud-hosted code-owned runtime path. [Certain]

Manual verification is still needed to confirm whether the Cloud Run runtime plus Gemini SDK satisfies the current judging interpretation. [Certain]

## Must Google Cloud Agent Builder Be Visibly Used

The public rules mention Google Cloud Agent Builder, so visible Google Cloud agent/runtime usage should be shown before final submission. [Likely]

The Arize resource page warns that visual Agent Builder alone is not supported for tracing integration and says the runtime must be code-owned. [Likely]

TraceLitmus should avoid claiming full Agent Builder production integration until a Google Cloud runtime or Agent Builder path is actually deployed and tested. [Certain]

## What Is Implemented Now

- Offline fixture audit works. [Certain]
- Phoenix MCP audit works locally against local Phoenix. [Certain]
- Streamlit UI works locally. [Certain]
- Gemini explanation boundary exists and preserves deterministic findings. [Certain]
- Gemini live verification worked during Phase 5 with a process-scoped key. [Certain]
- Gemini fallback warning works when credentials are absent. [Certain]
- Cloud Run deployment files exist. [Certain]

## What Remains Before Submission

- Choose and configure a hosted Phoenix endpoint, preferably Phoenix Cloud. [Likely]
- Deploy TraceLitmus to Cloud Run and test the deployed URL. [Certain]
- Confirm whether Cloud Run plus Gemini SDK is enough for the Agent Builder requirement, or add Google ADK, Agent Engine, or another accepted code-owned agent runtime layer. [Likely]
- Record a demo showing Phoenix MCP usage with reachable Phoenix data. [Certain]
