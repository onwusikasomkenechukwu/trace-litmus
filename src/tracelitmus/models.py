"""Pydantic models for Phoenix objects and audit output."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class PhoenixProject(BaseModel):
    id: str
    name: str
    description: str | None = None


class PhoenixPromptVersion(BaseModel):
    id: str
    prompt_id: str
    version_tag: str | None = None
    template: str
    model: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class PhoenixDataset(BaseModel):
    id: str
    name: str
    version: str


class PhoenixDatasetExample(BaseModel):
    id: str
    dataset_id: str
    input: dict[str, Any]
    expected_output: dict[str, Any]


class PhoenixExperiment(BaseModel):
    id: str
    dataset_id: str
    prompt_version_id: str | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    sample_size: int


class PhoenixTrace(BaseModel):
    id: str
    project_id: str
    span_count: int
    status: str


class EvidenceRef(BaseModel):
    object_type: Literal[
        "project",
        "prompt",
        "prompt_version",
        "dataset",
        "dataset_example",
        "experiment",
        "span",
        "span_annotation",
        "metric",
        "metadata",
    ]
    object_id: str
    label: str | None = None


class AuditFinding(BaseModel):
    rule_id: str
    severity: Literal["critical", "high", "medium", "low"]
    title: str
    description: str
    evidence: list[EvidenceRef] = Field(default_factory=list)
    recommended_fix: str


class AgentExplanation(BaseModel):
    executive_summary: str
    finding_explanations: list[str] = Field(default_factory=list)
    prioritized_next_steps: list[str] = Field(default_factory=list)


class AuditReport(BaseModel):
    project_id: str
    source: str = "Offline fixture"
    score: int
    score_start: int = 100
    score_penalty: int = 0
    severity_counts: dict[str, int] = Field(default_factory=dict)
    findings: list[AuditFinding] = Field(default_factory=list)
    summary: str
    agent_explanation: AgentExplanation | None = None
    agent_warning: str | None = None
    generated_at: datetime
