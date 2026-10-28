# Enterprise CRM Forensic Audit & Data Remediation API ⚡🛡️

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.9+-E92063.svg?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Multi--Stage-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An asynchronous enterprise microservice designed to ingest messy, corrupted CRM exports (**Salesforce** and **HubSpot** formats), quantify **Revenue at Risk** caused by pipeline rot, calculate a real-time **Data Health Score (0–100%)**, and stream back sanitized, production-ready datasets on demand in `< 150ms`.

![CRM Forensic Audit Cover](portfolio_assets/3_upwork_portfolio_cover.jpg)

---

## 📸 Live Telemetry & Data Transformation Proof

### 1. Executive Forensic Audit Dashboard (`85.7%` Hygiene Score | `$2.07B` Revenue at Risk)
![Forensic Dashboard](portfolio_assets/2_forensic_dashboard_ui.jpg)

### 2. Interactive OpenAPI / Swagger UI (`/docs`) & Real `AuditReportResponse` JSON
![Swagger UI Docs](portfolio_assets/1_swagger_ui_docs.jpg)

### 3. Before vs. After CSV Sanitization (`crm_deals_dirty.csv` $\rightarrow$ `crm_deals_sanitized.csv`)
![Before vs After CSV](portfolio_assets/4_data_transformation_before_after.jpg)

---

## 🏛️ System Architecture & Data Flow

```mermaid
flowchart TD
    subgraph Client ["Client Layer"]
        A["CRM Export (Salesforce / HubSpot CSV)<br>10,000+ Deals"]
    end

    subgraph API ["FastAPI Microservice (Port 8000)"]
        B["POST /api/v1/audit<br>or POST /api/v1/remediate"] --> C["In-Memory Buffer Ingestion<br>(io.BytesIO / Zero Disk I/O)"]
        C --> D["FastAPI Middleware<br>(X-Process-Time-Ms / CORS)"]
    end

    subgraph Engine ["High-Performance Audit & Remediation Engine"]
        D --> E["Vectorized Pandas Anomaly Masks<br>• Duplicates (Account+Stage+CloseDate)<br>• Amount Null/Negative<br>• Zombie Active Pipeline<br>• Non-RFC Emails / Phones<br>• UTF-8 Mojibake Encodings"]
        E --> F["Revenue at Risk Quantification<br>• Unrecognized Closed Won<br>• Fictitious Duplicate Pipeline<br>• Stale Active Deals"]
        E --> G["Weighted Hygiene Scoring (0–100%)<br>Critical (40%) | Warning (35%) | Minor (25%)"]
        E --> H["Automated Remediation Pipeline<br>• Cohort Median Imputation<br>• E.164 Phone Normalization<br>• ISO-8601 Date Reconciliation<br>• UTF-8 Mojibake Repair"]
    end

    subgraph Outputs ["Streaming Responses"]
        F --> I["JSON AuditReportResponse<br>200 OK (Executive Metrics & KPIs)"]
        G --> I
        H --> J["StreamingResponse (text/csv)<br>Sanitized Production Dataset"]
    end
```

---

## 🚀 Key Features

- **Sub-Second Vectorized Processing**: Audits and repairs 10,000 enterprise deal records in `< 150ms` using memory-mapped vector operations with no row-by-row iteration bottlenecks.
- **Revenue at Risk Quantification**: Automatically identifies fictitious pipeline from double webhook syncs, unrecognized revenue from Closed Won deals missing close dates, and stale pipeline from zombie deals.
- **Algorithmic Data Hygiene Scoring**: Weighted formula generating a continuous 0.0 to 100.0% pipeline health metric for executive reporting.
- **Automated Data Remediation**: Deduplication, stage-cohort statistical median imputation for deal amounts, RFC email sanitization, E.164 phone normalization, and automated routing of unassigned deals to a designated Sales Ops queue.
- **Enterprise-Grade Cloud Deployment**: Ready for 1-click Docker, Kubernetes, Render, or Railway deployment with non-root security compliance and health check telemetry.

---

## 📂 Project Structure

```
crm-forensic-audit-api/
├── app/
│   ├── __init__.py           # Package initializer
│   ├── audit_engine.py       # Vectorized Pandas forensic auditing & remediation engine
│   ├── main.py               # FastAPI microservice, middleware, and endpoints
│   └── schemas.py            # Strict Pydantic v2 schemas and data validation models
├── generate_mock_data.py     # Realistic 10,000-row enterprise CRM dataset generator
├── test_pipeline.py          # Automated integration test suite
├── Dockerfile                # Multi-stage lightweight production container
├── .dockerignore             # Optimized build context exclusion rules
├── render.yaml               # 1-Click Render infrastructure deployment config
├── requirements.txt          # Production dependencies
└── README.md                 # Complete system documentation
```

---

## ⚡ Quickstart: Local Setup & Running

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/your-username/crm-forensic-audit-api.git
cd crm-forensic-audit-api

python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Generate the 10,000-Row Messy CRM Dataset

```bash
python generate_mock_data.py
```
*Outputs: `crm_deals_dirty.csv` containing realistic CRM corruption (duplicates, null/negative amounts, zombie stages, malformed contacts, UTF-8 mojibake).*

### 3. Start the Microservice

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive Swagger UI at: **`http://localhost:8000/docs`**

---

## 🧪 Testing the API via cURL

### 1. System Health & Telemetry
```bash
curl -X GET http://localhost:8000/api/v1/health
```

### 2. Run Forensic Audit (Quantify Revenue at Risk)
```bash
curl -X POST http://localhost:8000/api/v1/audit \
  -H "accept: application/json" \
  -F "file=@crm_deals_dirty.csv"
```

### 3. Remediate & Download Cleaned Dataset
```bash
curl -X POST http://localhost:8000/api/v1/remediate \
  -F "file=@crm_deals_dirty.csv" \
  -F 'config={"deduplicate": true, "impute_amounts": true, "imputation_strategy": "median", "sanitize_emails": true, "normalize_phones": true, "normalize_dates": true, "resolve_orphan_owners": true}' \
  -o crm_deals_sanitized.csv
```

---

## 🚢 Production Deployment

### Option A: Render.com (3 Minutes, Zero-Cost)
1. Push this repository to GitHub.
2. Sign in to [Render.com](https://render.com) and click **New + > Web Service**.
3. Connect your repository. Render automatically reads `render.yaml`.
4. Click **Deploy Web Service** to obtain a public HTTPS URL (e.g., `https://crm-audit-api.onrender.com/docs`).

### Option B: Railway.app
1. Link your GitHub repository in Railway.
2. Railway detects the `Dockerfile` automatically.
3. Deploy in seconds.

### Option C: Docker Container
```bash
docker build -t crm-audit-api:latest .
docker run -p 8000:8000 crm-audit-api:latest
```

---

## 📄 License
MIT License. Open-source for commercial and enterprise integration.
