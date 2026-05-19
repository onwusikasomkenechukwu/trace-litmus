"""Verify the TraceLitmus Gemini explanation boundary."""

from __future__ import annotations

from argparse import ArgumentParser
from datetime import UTC, datetime
from os import environ
from pathlib import Path
from sys import exit
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tracelitmus.agent import attach_agent_explanation
from tracelitmus.models import AuditFinding, AuditReport, EvidenceRef
from tracelitmus.phoenix_client import load_env_file


def _parser() -> ArgumentParser:
    parser = ArgumentParser(description="Verify the Gemini explanation layer.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--require-live", action="store_true")
    mode.add_argument("--allow-fallback", action="store_true")
    return parser


def _provider() -> str:
    if environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in {"1", "true", "yes"}:
        return "Vertex AI Gemini"
    return "Gemini API"


def _sample_report() -> AuditReport:
    finding = AuditFinding(
        rule_id="missing_baseline",
        severity="medium",
        title="No baseline experiment is linked",
        description="The experiment reports metrics without naming the baseline run it should be compared against.",
        evidence=[
            EvidenceRef(
                object_type="experiment",
                object_id="exp_verify_gemini",
                label="missing baseline_experiment_id",
            )
        ],
        recommended_fix="Store a baseline experiment ID or reference run in metadata.",
    )
    return AuditReport(
        project_id="verify-gemini",
        source="Verification sample",
        score=94,
        score_start=100,
        score_penalty=6,
        severity_counts={"critical": 0, "high": 0, "medium": 1, "low": 0},
        findings=[finding],
        summary="Verification report for the Gemini explanation boundary.",
        generated_at=datetime.now(UTC),
    )


def main() -> int:
    args = _parser().parse_args()
    load_env_file()
    report = _sample_report()
    attach_agent_explanation(report, enabled=True)
    fallback_used = report.agent_explanation is None

    print(f"provider: {_provider()}")
    print(f"fallback_used: {str(fallback_used).lower()}")
    if report.agent_explanation:
        print(f"executive_summary: {report.agent_explanation.executive_summary}")
        print("limitations: Gemini output is prose only; deterministic audit fields are unchanged.")
    else:
        print("executive_summary: unavailable")
        print(f"limitations: {report.agent_warning}")

    if args.require_live and fallback_used:
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
