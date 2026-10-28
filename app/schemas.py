"""
Enterprise CRM Data Schemas & Forensic Models (Pydantic v2)
===========================================================
Defines strict validation rules, forensic anomaly breakdowns,
executive risk reporting schemas, and remediation configuration models.

Author: Principal Backend Engineer & Senior Data Architect
"""

from datetime import datetime
from typing import Optional, List, Dict, Literal
import re
from pydantic import BaseModel, Field, field_validator, ConfigDict


class DealRecord(BaseModel):
    """
    Field-level validation rules for an individual CRM Deal record.
    Adheres strictly to Pydantic v2 standards.
    """
    model_config = ConfigDict(from_attributes=True, extra="ignore", str_strip_whitespace=True)

    deal_id: str = Field(..., description="Unique alphanumeric identifier for CRM deal")
    deal_name: str = Field(..., min_length=3, description="Deal title or account initiative name")
    account_name: str = Field(..., min_length=2, description="Target enterprise account name")
    contact_email: Optional[str] = Field(None, description="Primary prospect contact email")
    contact_phone: Optional[str] = Field(None, description="Primary prospect phone number")
    deal_stage: str = Field(
        ...,
        description="Current sales pipeline stage (Discovery, Qualification, Proposal/Quote, Negotiation/Review, Closed Won, Closed Lost)"
    )
    amount: Optional[float] = Field(None, description="Total contracted or forecasted deal value in USD")
    close_date: Optional[str] = Field(None, description="Targeted or actual deal close date (ISO YYYY-MM-DD)")
    deal_owner: Optional[str] = Field(None, description="Assigned Account Executive or SDR")
    lead_source: Optional[str] = Field(None, description="Channel attribution")
    created_at: Optional[str] = Field(None, description="Record creation timestamp")

    @field_validator("deal_stage")
    @classmethod
    def validate_stage(cls, v: str) -> str:
        valid_stages = {
            "discovery", "qualification", "proposal/quote",
            "negotiation/review", "closed won", "closed lost"
        }
        if v.lower() not in valid_stages:
            raise ValueError(f"Invalid deal stage: '{v}'. Must be one of {valid_stages}")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError(f"Deal amount cannot be negative: {v}")
        return v


class AnomalyDetail(BaseModel):
    """Specific anomaly category metrics including occurrence count and dollar-value impact."""
    count: int = Field(0, description="Total anomalous records detected")
    monetary_impact_usd: float = Field(0.0, description="Estimated total gross revenue impacted")
    severity: Literal["CRITICAL", "WARNING", "MINOR"] = Field("WARNING", description="Risk tier")


class AnomalyBreakdown(BaseModel):
    """Detailed forensic categorization of detected CRM data corruption."""
    duplicate_deals: AnomalyDetail = Field(
        ..., description="Exact duplicates across account, stage, and close date causing inflated pipeline"
    )
    invalid_amounts: AnomalyDetail = Field(
        ..., description="Deals with missing, zero, or negative dollar amounts"
    )
    stage_mismatches: AnomalyDetail = Field(
        ..., description="Closed Won without close dates, or active deals with expired close dates (Zombie pipeline)"
    )
    malformed_emails: AnomalyDetail = Field(
        ..., description="Contacts with invalid TLD, missing @, or non-RFC syntax"
    )
    malformed_phones: AnomalyDetail = Field(
        ..., description="Truncated, non-numeric, or unparseable phone numbers"
    )
    unassigned_owners: AnomalyDetail = Field(
        ..., description="Deals missing an accountable sales rep or marked unassigned"
    )
    corrupted_encodings: AnomalyDetail = Field(
        ..., description="Character encoding artifacts and UTF-8 mojibake (e.g., Ã©, Ã¼)"
    )
    non_standard_dates: AnomalyDetail = Field(
        ..., description="Dates violating ISO-8601 YYYY-MM-DD format"
    )


class ExecutiveSummary(BaseModel):
    """High-level risk and pipeline integrity synthesis for CROs and VP of Sales Ops."""
    health_classification: Literal["CRITICAL RISK", "NEEDS ATTENTION", "MODERATE", "ENTERPRISE GRADE"] = Field(
        ..., description="Qualitative pipeline health tier"
    )
    primary_revenue_threat: str = Field(..., description="The #1 single anomaly driving monetary pipeline exposure")
    projected_recovery_percentage: float = Field(..., description="Projected pipeline integrity recovered post-remediation")
    actionable_recommendations: List[str] = Field(..., description="Strategic recommendations to eliminate pipeline leakages")


class AuditReportResponse(BaseModel):
    """
    Standardized Enterprise Audit Response schema.
    Quantifies revenue at risk, health scoring, and forensic details.
    """
    hygiene_score: float = Field(..., ge=0.0, le=100.0, description="Algorithmic Data Health Score (0.0 to 100.0%)")
    total_records: int = Field(..., description="Total rows ingested from CRM export")
    clean_records: int = Field(..., description="Records fully passing all validation constraints")
    corrupted_records: int = Field(..., description="Records exhibiting at least one critical or warning anomaly")
    total_pipeline_value: float = Field(..., description="Gross total dollar amount found in dataset")
    revenue_at_risk: float = Field(..., description="Total monetary pipeline contaminated by corrupt deal logic")
    risk_percentage: float = Field(..., description="Percentage of pipeline dollars currently compromised")
    anomalies_by_severity: Dict[str, int] = Field(
        ..., description="Aggregation of total errors grouped into CRITICAL, WARNING, and MINOR"
    )
    anomaly_breakdown: AnomalyBreakdown = Field(..., description="Granular forensic metrics per failure category")
    executive_summary: ExecutiveSummary = Field(..., description="C-Suite executive synthesis and pipeline recommendations")
    audit_timestamp: datetime = Field(default_factory=datetime.utcnow, description="UTC timestamp of audit completion")
    execution_time_ms: float = Field(..., description="Total in-memory processing latency in milliseconds")


class RemediationConfig(BaseModel):
    """
    Configuration parameters for automated, vectorized data remediation.
    Provides fine-grained control over algorithmic repair rules.
    """
    deduplicate: bool = Field(True, description="Remove duplicate deal entries, retaining highest-confidence record")
    impute_amounts: bool = Field(True, description="Impute missing or negative amounts using cohort statistical median")
    imputation_strategy: Literal["median", "mean", "zero"] = Field("median", description="Statistical imputation strategy")
    sanitize_emails: bool = Field(True, description="Clean whitespace, lowercase, and flag/sanitize malformed emails")
    normalize_phones: bool = Field(True, description="Standardize phone numbers into clean E.164-compatible formatting")
    normalize_dates: bool = Field(True, description="Coerce all valid date variants into strict ISO-8601 (YYYY-MM-DD)")
    resolve_orphan_owners: bool = Field(True, description="Assign unallocated deals to fallback Sales Operations routing pool")
    default_owner: str = Field("Sales Operations Pool", description="Default assignee for unassigned deals")
    fix_encoding: bool = Field(True, description="Detect and repair UTF-8 mojibake characters")
    reconcile_stage_dates: bool = Field(True, description="Align Closed Won dates and flag zombie deals")


class HealthResponse(BaseModel):
    """Service health and diagnostic status."""
    status: str = Field("healthy", description="API operational status")
    service: str = Field("Enterprise CRM Forensic Audit & Data Remediation API", description="Microservice name")
    version: str = Field("1.0.0", description="API release version")
    uptime_seconds: float = Field(..., description="Service uptime duration")
    memory_usage_mb: float = Field(..., description="Current process RAM usage in Megabytes")
    environment: str = Field("production", description="Runtime environment")
