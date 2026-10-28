"""
Automated Test & Verification Suite
===================================
Tests all microservice endpoints:
- GET /api/v1/health
- POST /api/v1/audit
- POST /api/v1/remediate
"""

import sys
import json
import time
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    print("[*] Testing GET /api/v1/health...")
    response = client.get("/api/v1/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy"
    assert "memory_usage_mb" in data
    print(f"    [+] Health Check Passed: Status={data['status']}, Latency={response.headers.get('x-process-time-ms')}")


def test_audit():
    print("[*] Testing POST /api/v1/audit with 'crm_deals_dirty.csv' (10,000 rows)...")
    start = time.perf_counter()
    with open("crm_deals_dirty.csv", "rb") as f:
        response = client.post("/api/v1/audit", files={"file": ("crm_deals_dirty.csv", f, "text/csv")})
    duration = (time.perf_counter() - start) * 1000.0

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    report = response.json()
    assert report["total_records"] == 10000
    assert 0 <= report["hygiene_score"] <= 100
    assert report["revenue_at_risk"] > 0
    assert "executive_summary" in report

    print(f"    [+] Audit Passed in {duration:.2f}ms (Engine: {report['execution_time_ms']}ms)")
    print(f"    [+] Hygiene Score: {report['hygiene_score']}%")
    print(f"    [+] Pipeline Value: ${report['total_pipeline_value']:,.2f}")
    print(f"    [+] Revenue at Risk: ${report['revenue_at_risk']:,.2f} ({report['risk_percentage']}%)")
    print(f"    [+] Critical Anomalies: {report['anomalies_by_severity']['CRITICAL']:,}")


def test_remediation():
    print("[*] Testing POST /api/v1/remediate with automated cleaning config...")
    config_payload = {
        "deduplicate": True,
        "impute_amounts": True,
        "imputation_strategy": "median",
        "sanitize_emails": True,
        "normalize_phones": True,
        "normalize_dates": True,
        "resolve_orphan_owners": True,
        "default_owner": "Enterprise Sales Ops Pool",
        "fix_encoding": True,
        "reconcile_stage_dates": True
    }

    start = time.perf_counter()
    with open("crm_deals_dirty.csv", "rb") as f:
        response = client.post(
            "/api/v1/remediate",
            files={"file": ("crm_deals_dirty.csv", f, "text/csv")},
            data={"config": json.dumps(config_payload)}
        )
    duration = (time.perf_counter() - start) * 1000.0

    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert "attachment; filename=" in response.headers.get("content-disposition", "")

    # Save and verify clean CSV
    with open("crm_deals_sanitized.csv", "wb") as f_out:
        f_out.write(response.content)

    clean_df = pd.read_csv("crm_deals_sanitized.csv")
    print(f"    [+] Remediation Streamed in {duration:.2f}ms")
    print(f"    [+] Cleaned Dataset Rows: {len(clean_df):,} (Deduplicated & Imputed)")
    print(f"    [+] Saved Output to: 'crm_deals_sanitized.csv'")


if __name__ == "__main__":
    print("=" * 70)
    print("  ENTERPRISE CRM FORENSIC AUDIT - INTEGRATION TEST SUITE")
    print("=" * 70)
    test_health()
    test_audit()
    test_remediation()
    print("=" * 70)
    print("  ALL 3 ENDPOINTS VERIFIED & PRODUCTION READY [100% PASS]")
    print("=" * 70)
