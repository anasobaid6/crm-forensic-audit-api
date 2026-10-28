"""
Enterprise CRM Deals Dataset Generator
======================================
Generates a realistic, messy 10,000-row enterprise CRM dataset ('crm_deals_dirty.csv')
simulating authentic pipeline corruption, syncing failures, and human entry errors
found in Salesforce and HubSpot instances.

Author: Principal Data Architect & Senior Backend Engineer
Target: Flagship Upwork Portfolio - Enterprise CRM Forensic Audit & Data Remediation API
"""

import random
import csv
import sys
from datetime import datetime, timedelta
import numpy as np
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

OUTPUT_FILE = "crm_deals_dirty.csv"
ROW_COUNT = 10000

DEAL_STAGES = [
    "Discovery",
    "Qualification",
    "Proposal/Quote",
    "Negotiation/Review",
    "Closed Won",
    "Closed Lost"
]

LEAD_SOURCES = [
    "Inbound Enterprise",
    "Outbound SDR",
    "Partner Referral",
    "Executive Network",
    "Gartner Review",
    "Annual Summit",
    "Organic Search"
]

SALES_REPS = [
    "Sarah Jenkins",
    "Michael Chang",
    "Elena Rostova",
    "Marcus Vance",
    "Amina Al-Mansoor",
    "David K. Miller",
    "Chloe Beauchamp",
    "Rajesh Patel"
]

ENTERPRISE_PRODUCTS = [
    "Cloud Infrastructure Overhaul",
    "Zero-Trust Cybersecurity Suite",
    "AI Predictive Analytics Platform",
    "Enterprise Data Lake Migration",
    "Automated CI/CD Pipeline",
    "Customer 360 CRM Integration",
    "Supply Chain Optimization Engine",
    "Compliance & Governance Module"
]

CORRUPTED_ACCOUNTS = [
    ("Société Générale", "SociÃ©tÃ© GÃ©nÃ©rale"),
    ("Zürich Financial Group", "ZÃ¼rich Financial Group"),
    ("Müller & Schmidt Logistik", "MÃ¼ller & Schmidt Logistik"),
    ("Crédit Agricole", "CrÃ©dit Agricole"),
    ("København Shipping AS", "KÃ¸benhavn Shipping AS"),
    ("São Paulo Fintech Ltd", "SÃ£o Paulo Fintech Ltd"),
    ("Düsseldorf Automotive", "DÃ¼sseldorf Automotive")
]


def generate_realistic_deal(index: int, reference_date: datetime):
    """Generates a clean baseline CRM deal record."""
    account_clean, _ = random.choice(CORRUPTED_ACCOUNTS) if random.random() < 0.1 else (fake.company(), None)
    product = random.choice(ENTERPRISE_PRODUCTS)
    quarter = f"Q{random.randint(1, 4)} {random.choice([2024, 2025])}"
    deal_name = f"{account_clean} - {product} ({quarter})"
    
    stage = random.choice(DEAL_STAGES)
    
    # Baseline normal amount between $15,000 and $650,000
    amount = round(random.uniform(15000, 650000), 2)
    
    # Created date in the past 12-18 months
    created_dt = reference_date - timedelta(days=random.randint(30, 450))
    created_at = created_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Logical close date relative to created_at
    if stage == "Closed Won":
        close_dt = created_dt + timedelta(days=random.randint(20, 90))
    elif stage == "Closed Lost":
        close_dt = created_dt + timedelta(days=random.randint(15, 60))
    else:
        # Active deals close in future relative to created_dt
        close_dt = reference_date + timedelta(days=random.randint(10, 180))
        
    close_date = close_dt.strftime("%Y-%m-%d")
    
    first_name = fake.first_name()
    last_name = fake.last_name()
    domain = account_clean.lower().replace(" ", "").replace(",", "").replace(".", "").replace("-", "")[:12] + ".com"
    email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
    phone = f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
    owner = random.choice(SALES_REPS)
    lead_source = random.choice(LEAD_SOURCES)
    
    return {
        "deal_id": f"DL-{10000 + index}",
        "deal_name": deal_name,
        "account_name": account_clean,
        "contact_email": email,
        "contact_phone": phone,
        "deal_stage": stage,
        "amount": amount,
        "close_date": close_date,
        "deal_owner": owner,
        "lead_source": lead_source,
        "created_at": created_at
    }


def inject_anomalies(records: list[dict], reference_date: datetime):
    """
    Injects high-impact enterprise data corruptions into the dataset:
    - Corrupted UTF-8 encodings (mojibake)
    - Malformed emails and invalid phone numbers
    - Null, zero, or negative deal values
    - Stage-date logic violations (Closed Won with missing close date, Zombie deals)
    - Non-standard date formats
    - Unassigned / Orphan deal owners
    """
    total = len(records)
    print(f"[*] Ingesting {total} clean deal records and synthesizing realistic pipeline corruption...")

    # 1. Corrupted UTF-8 character encoding (~4% of rows)
    corrupt_encoding_indices = random.sample(range(total), int(total * 0.04))
    for idx in corrupt_encoding_indices:
        _, corrupted_val = random.choice(CORRUPTED_ACCOUNTS)
        records[idx]["account_name"] = corrupted_val
        records[idx]["deal_name"] = f"{corrupted_val} - Enterprise Expansion"

    # 2. Malformed emails (~6% of rows)
    malformed_email_indices = random.sample(range(total), int(total * 0.06))
    for idx in malformed_email_indices:
        err_type = random.choice(["no_at", "invalid_tld", "double_at", "trailing_dot", "spaces"])
        curr_email = records[idx]["contact_email"]
        name_part = curr_email.split("@")[0] if "@" in curr_email else "user"
        if err_type == "no_at":
            records[idx]["contact_email"] = f"{name_part}enterprise.com"
        elif err_type == "invalid_tld":
            records[idx]["contact_email"] = f"{name_part}@corp_null"
        elif err_type == "double_at":
            records[idx]["contact_email"] = f"{name_part}@@global.org"
        elif err_type == "trailing_dot":
            records[idx]["contact_email"] = f"{curr_email}."
        elif err_type == "spaces":
            records[idx]["contact_email"] = f" {name_part} @company.com "

    # 3. Truncated & invalid phone numbers (~5% of rows)
    malformed_phone_indices = random.sample(range(total), int(total * 0.05))
    for idx in malformed_phone_indices:
        err_type = random.choice(["truncated", "letters", "empty", "special_chars"])
        if err_type == "truncated":
            records[idx]["contact_phone"] = str(random.randint(100, 9999))
        elif err_type == "letters":
            records[idx]["contact_phone"] = "+1-800-CALL-ACME"
        elif err_type == "empty":
            records[idx]["contact_phone"] = ""
        elif err_type == "special_chars":
            records[idx]["contact_phone"] = "###-UNKNOWN-###"

    # 4. Null, zero, or negative amounts (~7% of rows)
    bad_amount_indices = random.sample(range(total), int(total * 0.07))
    for idx in bad_amount_indices:
        err_type = random.choice(["null", "zero", "negative"])
        if err_type == "null":
            records[idx]["amount"] = ""
        elif err_type == "zero":
            records[idx]["amount"] = 0.0
        elif err_type == "negative":
            records[idx]["amount"] = -round(random.uniform(5000, 120000), 2)

    # 5. Logically impossible stages & zombie deals (~8% of rows)
    # Case A: Closed Won with missing or empty close_date
    won_indices = [i for i, r in enumerate(records) if r["deal_stage"] == "Closed Won"]
    closed_won_no_date = random.sample(won_indices, min(len(won_indices), int(total * 0.03)))
    for idx in closed_won_no_date:
        records[idx]["close_date"] = ""

    # Case B: Active stage (Discovery / Negotiation) with past close_date (Zombie deals)
    active_indices = [i for i, r in enumerate(records) if r["deal_stage"] in ["Discovery", "Proposal/Quote", "Negotiation/Review"]]
    zombie_indices = random.sample(active_indices, min(len(active_indices), int(total * 0.05)))
    for idx in zombie_indices:
        expired_date = reference_date - timedelta(days=random.randint(60, 300))
        records[idx]["close_date"] = expired_date.strftime("%Y-%m-%d")

    # 6. Non-standard date formats (~6% of rows)
    non_std_date_indices = random.sample(range(total), int(total * 0.06))
    for idx in non_std_date_indices:
        if records[idx]["close_date"]:
            try:
                dt = datetime.strptime(records[idx]["close_date"], "%Y-%m-%d")
                format_choice = random.choice(["%m/%d/%Y", "%d-%m-%Y", "%Y.%m.%d", "%d/%m/%Y"])
                records[idx]["close_date"] = dt.strftime(format_choice)
            except ValueError:
                pass

    # 7. Unassigned deal owners (~5% of rows)
    unassigned_indices = random.sample(range(total), int(total * 0.05))
    for idx in unassigned_indices:
        records[idx]["deal_owner"] = random.choice(["", "Unassigned", "None", "TBD", "N/A"])

    # 8. Duplicate deals (inject ~350 exact duplicate rows across account, stage, close date)
    duplicate_source_indices = random.sample(range(total - 400), 350)
    for src_idx in duplicate_source_indices:
        target_idx = random.randint(0, total - 1)
        if target_idx != src_idx:
            # Overwrite target with exact duplicate attributes while retaining separate deal_id or matching it
            records[target_idx]["account_name"] = records[src_idx]["account_name"]
            records[target_idx]["deal_stage"] = records[src_idx]["deal_stage"]
            records[target_idx]["close_date"] = records[src_idx]["close_date"]
            records[target_idx]["amount"] = records[src_idx]["amount"]
            records[target_idx]["deal_name"] = records[src_idx]["deal_name"]

    print(f"[+] Successfully injected anomalies across pipeline stages and attributes.")


def main():
    print("=" * 70)
    print("  ENTERPRISE CRM FORENSIC AUDIT - SYNTHETIC DATA GENERATOR")
    print("=" * 70)
    
    reference_date = datetime(2025, 1, 15)
    print(f"[*] Benchmark Reference Date: {reference_date.strftime('%Y-%m-%d')}")
    print(f"[*] Target Generation: {ROW_COUNT:,} CRM deal records...")

    records = [generate_realistic_deal(i, reference_date) for i in range(ROW_COUNT)]
    inject_anomalies(records, reference_date)

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
        "created_at"
    ]

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[+] File successfully generated: '{OUTPUT_FILE}' ({ROW_COUNT:,} rows).")
    print("=" * 70)


if __name__ == "__main__":
    main()
