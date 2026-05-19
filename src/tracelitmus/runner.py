"""Small report runner facade used by the CLI, UI, and smoke scripts."""

from __future__ import annotations

from pathlib import Path

from .cli import run_audit, run_mcp_audit


def run_report(
    *,
    source: str,
    project: str,
    output: str,
    gemini_explanation: bool = False,
) -> Path:
    if source == "mcp":
        return run_mcp_audit(
            project=project,
            output=output,
            gemini_explanation=gemini_explanation,
        )
    return run_audit(
        project=project,
        offline=True,
        output=output,
        gemini_explanation=gemini_explanation,
    )
