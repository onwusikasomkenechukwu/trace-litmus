# TraceLitmus Final Demo Script

## 0:00-0:15 - Problem

LLM evaluation dashboards can look clean while hiding reproducibility failures: missing baselines, prompt drift, dataset drift, and unsupported comparison claims.

## 0:15-0:35 - Hosted App

Open the Cloud Run URL:
[https://tracelitmus-vemlexqp2q-uc.a.run.app](https://tracelitmus-vemlexqp2q-uc.a.run.app)

Show hosted offline mode and explain that this proves the judge-facing app is deployed.

Say explicitly:

The hosted app proves deployability. Hosted Phoenix MCP still requires a reachable Phoenix endpoint and is not claimed here.

## 0:35-0:55 - Local Phoenix MCP Path

Switch to local Streamlit or CLI with Phoenix running. Select Phoenix MCP or show the CLI command. Project: `tracelitmus-demo`.

Say explicitly:

This local segment proves the Phoenix MCP integration path.

## 0:55-1:25 - Run Audit

Run MCP audit. Show `Source: Phoenix MCP`.

## 1:25-1:55 - Finding

Show `missing_baseline`. Show evidence:

`experiment:RXhwZXJpbWVudDoy`

and

`metadata:baseline_experiment_id`

## 1:55-2:25 - Gemini Explanation

Enable or show Gemini explanation.

Say explicitly:

Gemini explains the deterministic finding; it cannot change score, severity, rule ID, or evidence refs.

## 2:25-2:45 - Download Report

Show Markdown download or generated report file.

## 2:45-3:00 - Close

TraceLitmus turns Phoenix evaluation artifacts into reproducibility evidence before a team trusts an LLM eval claim.

## Note

If hosted Phoenix becomes available before submission, replace the local MCP segment with hosted MCP in the Cloud Run app.

