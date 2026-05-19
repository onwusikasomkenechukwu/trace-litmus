"""Gemini explanation layer for TraceLitmus reports.

Gemini is a narrator, not the judge. Deterministic Python code owns findings,
evidence refs, severities, and scoring. This module sends only sanitized audit
metadata to Gemini and stores returned prose in separate report fields.
"""

from __future__ import annotations

from json import JSONDecodeError, dumps, loads
from os import environ
from typing import Any

from pydantic import ValidationError

from .models import AgentExplanation, AuditReport
from .phoenix_client import load_env_file


class AgentExplanationUnavailable(RuntimeError):
    """Raised when Gemini explanation generation is not configured or fails."""


def sanitized_audit_payload(report: AuditReport) -> dict[str, Any]:
    """Return the only payload Gemini is allowed to see."""

    return {
        "project_id": report.project_id,
        "source": report.source,
        "score": report.score,
        "score_start": report.score_start,
        "score_penalty": report.score_penalty,
        "severity_counts": report.severity_counts,
        "summary": report.summary,
        "findings": [
            {
                "rule_id": finding.rule_id,
                "severity": finding.severity,
                "title": finding.title,
                "description": finding.description,
                "evidence": [
                    {
                        "object_type": evidence.object_type,
                        "object_id": evidence.object_id,
                        "label": evidence.label,
                    }
                    for evidence in finding.evidence
                ],
                "recommended_fix": finding.recommended_fix,
            }
            for finding in report.findings
        ],
    }


def _prompt(payload: dict[str, Any]) -> str:
    return (
        "You are the TraceLitmus explanation layer. "
        "Explain deterministic audit findings without changing them. "
        "Do not invent evidence. Do not create, remove, rewrite, or reinterpret object IDs. "
        "Return only JSON with keys executive_summary, finding_explanations, prioritized_next_steps. "
        "finding_explanations and prioritized_next_steps must be arrays of short strings. "
        "Use plain language for a hackathon demo audience.\n\n"
        f"Sanitized audit payload:\n{dumps(payload, indent=2)}"
    )


def _client() -> Any:
    try:
        from google import genai
    except ModuleNotFoundError as exc:
        raise AgentExplanationUnavailable(
            "Gemini explanation requested, but `google-genai` is not installed."
        ) from exc

    use_vertex = environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in {"1", "true", "yes"}
    if use_vertex:
        project = environ.get("GOOGLE_CLOUD_PROJECT")
        location = environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
        if not project:
            raise AgentExplanationUnavailable(
                "Gemini explanation requested with Vertex AI, but GOOGLE_CLOUD_PROJECT is not set."
            )
        return genai.Client(vertexai=True, project=project, location=location)

    api_key = environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise AgentExplanationUnavailable(
            "Gemini explanation requested, but GOOGLE_API_KEY is not set."
        )
    return genai.Client(api_key=api_key)


def generate_gemini_explanation(report: AuditReport) -> AgentExplanation:
    """Generate prose from sanitized findings while preserving deterministic fields."""

    load_env_file()
    model = environ.get("GOOGLE_GENAI_MODEL") or environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    payload = sanitized_audit_payload(report)
    client = _client()
    try:
        response = client.models.generate_content(
            model=model,
            contents=_prompt(payload),
            config={"response_mime_type": "application/json"},
        )
    except Exception as exc:
        raise AgentExplanationUnavailable(f"Gemini explanation call failed: {exc}") from exc

    text = getattr(response, "text", "") or ""
    if text.strip().startswith("```"):
        text = text.strip().strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    try:
        data = loads(text)
    except JSONDecodeError as exc:
        raise AgentExplanationUnavailable(
            f"Gemini returned non-JSON explanation text: {text[:500]}"
        ) from exc
    try:
        return AgentExplanation(**data)
    except ValidationError as exc:
        raise AgentExplanationUnavailable(f"Gemini explanation shape was invalid: {exc}") from exc


def attach_agent_explanation(report: AuditReport, *, enabled: bool) -> AuditReport:
    """Attach Gemini prose or a visible warning without changing audit facts."""

    if not enabled:
        return report
    try:
        report.agent_explanation = generate_gemini_explanation(report)
        report.agent_warning = None
    except AgentExplanationUnavailable as exc:
        report.agent_explanation = None
        report.agent_warning = str(exc)
    return report
