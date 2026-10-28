"""
================================================================================
Enterprise CRM Dirty Dataset Generator
Author: Principal Python Backend Engineer
Description: Generates messy enterprise CRM datasets ('crm_sample_dirty.csv' and
             'crm_deals_dirty.csv') matching the exact schema expected by the
             FastAPI Forensic Audit & Data Hygiene engine.
================================================================================
"""

import csv
from datetime import datetime
from pathlib import Path
import generate_mock_data

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_OUTPUT = BASE_DIR / "crm_sample_dirty.csv"
ROW_COUNT = 5000


def generate_dirty_crm(output_path: Path = SAMPLE_OUTPUT, count: int = ROW_COUNT):
    print(f"[*] Generating {count:,} dirty CRM deal records for: {output_path.name}...")
    reference_date = datetime(2025, 1, 15)
    records = [generate_mock_data.generate_realistic_deal(i, reference_date) for i in range(count)]
    generate_mock_data.inject_anomalies(records, reference_date)

    fieldnames = [
        "deal_id",
        "deal_name",
        "account_name",
        "contact_email",
        "contact_phone",
        "deal_stage",
        "amount",
        "close_date",
        "deal_owner",
        "lead_source",
        "created_at",
    ]

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[+] Successfully exported {count:,} records to '{output_path}'.")


if __name__ == "__main__":
    generate_dirty_crm()
