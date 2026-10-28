"""
Executive Forensic Audit Web Dashboard UI
=========================================
Self-contained, responsive, ultra-premium dark-mode dashboard
providing one-click interactive demonstration, drag-and-drop CSV audit,
live Data Health Score visualization, and automated CSV streaming download.

Author: Principal Backend Engineer & Senior Data Architect
"""

def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enterprise CRM Forensic Audit & Remediation Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #080c14;
      --card-bg: rgba(15, 23, 42, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover: rgba(30, 41, 59, 0.85);
      --cyan: #06b6d4;
      --cyan-glow: rgba(6, 182, 212, 0.25);
      --blue: #3b82f6;
      --purple: #8b5cf6;
      --emerald: #10b981;
      --rose: #f43f5e;
      --amber: #f59e0b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 15% 20%, rgba(6, 182, 212, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%);
      color: var(--text-main);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      line-height: 1.5;
    }

    /* Top Navigation */
    header {
      border-bottom: 1px solid var(--card-border);
      backdrop-filter: blur(12px);
      background: rgba(8, 12, 20, 0.8);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .nav-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      text-decoration: none;
      color: var(--text-main);
    }

    .brand-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--cyan), var(--purple));
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.3rem;
      box-shadow: 0 0 15px var(--cyan-glow);
    }

    .brand-title {
      font-family: 'Outfit', sans-serif;
      font-size: 1.2rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .brand-subtitle {
      font-size: 0.75rem;
      color: var(--cyan);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .badge-live {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.35rem 0.75rem;
      border-radius: 9999px;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--emerald);
      font-size: 0.8rem;
      font-weight: 600;
    }

    .badge-live::before {
      content: "";
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--emerald);
      box-shadow: 0 0 8px var(--emerald);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.9); }
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 500;
      text-decoration: none;
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
    }

    /* Main Container */
    main {
      max-width: 1400px;
      margin: 0 auto;
      padding: 2.5rem 2rem 5rem 2rem;
    }

    /* Hero Section */
    .hero {
      text-align: center;
      max-width: 800px;
      margin: 0 auto 3rem auto;
    }

    .hero h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 2.75rem;
      font-weight: 800;
      line-height: 1.15;
      margin-bottom: 1rem;
      background: linear-gradient(135deg, #fff 40%, var(--cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -0.03em;
    }

    .hero p {
      font-size: 1.1rem;
      color: var(--text-muted);
      margin-bottom: 2rem;
    }

    /* Ingestion Action Box */
    .upload-container {
      background: var(--card-bg);
      border: 2px dashed var(--card-border);
      border-radius: 16px;
      padding: 2.5rem 2rem;
      text-align: center;
      transition: all 0.3s ease;
      position: relative;
      margin-bottom: 3rem;
    }

    .upload-container:hover, .upload-container.dragover {
      border-color: var(--cyan);
      box-shadow: 0 0 30px var(--cyan-glow);
    }

    .upload-icon {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }

    .upload-title {
      font-size: 1.2rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }

    .upload-desc {
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-bottom: 1.5rem;
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--cyan), var(--blue));
      color: #fff;
      border: none;
      padding: 0.75rem 1.75rem;
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(6, 182, 212, 0.35);
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
    }

    .sample-btn {
      background: rgba(139, 92, 246, 0.15);
      color: #c4b5fd;
      border: 1px solid rgba(139, 92, 246, 0.3);
      padding: 0.75rem 1.75rem;
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      margin-left: 1rem;
      transition: all 0.2s ease;
    }

    .sample-btn:hover {
      background: rgba(139, 92, 246, 0.25);
      border-color: rgba(139, 92, 246, 0.5);
      color: #fff;
    }

    /* Results Dashboard Grid */
    #dashboard-results {
      display: none;
      animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .kpi-grid {
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 1.5rem;
      margin-bottom: 2rem;
    }

    @media (max-width: 992px) {
      .kpi-grid {
        grid-template-columns: 1fr;
      }
    }

    /* Score Card */
    .score-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 2rem;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }

    .score-ring {
      position: relative;
      width: 170px;
      height: 170px;
      margin-bottom: 1.5rem;
    }

    .score-ring svg {
      width: 170px;
      height: 170px;
      transform: rotate(-90deg);
    }

    .score-ring circle {
      fill: none;
      stroke-width: 12;
      stroke-linecap: round;
    }

    .score-ring .bg {
      stroke: rgba(255, 255, 255, 0.05);
    }

    .score-ring .progress {
      stroke: var(--cyan);
      stroke-dasharray: 440;
      stroke-dashoffset: 440;
      transition: stroke-dashoffset 1.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .score-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-family: 'Outfit', sans-serif;
      font-size: 2.5rem;
      font-weight: 800;
    }

    .score-label {
      font-size: 0.9rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
    }

    .score-classification {
      margin-top: 0.5rem;
      padding: 0.35rem 1rem;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 700;
      background: rgba(6, 182, 212, 0.15);
      color: var(--cyan);
      border: 1px solid rgba(6, 182, 212, 0.3);
    }

    /* Metrics Grid */
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.25rem;
    }

    @media (max-width: 600px) {
      .metrics-grid {
        grid-template-columns: 1fr;
      }
    }

    .metric-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: border-color 0.2s ease;
    }

    .metric-card:hover {
      border-color: rgba(255, 255, 255, 0.2);
    }

    .metric-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }

    .metric-title {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .metric-icon {
      font-size: 1.25rem;
    }

    .metric-value {
      font-family: 'Outfit', sans-serif;
      font-size: 1.85rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .metric-footer {
      font-size: 0.8rem;
      margin-top: 0.5rem;
      color: var(--text-muted);
    }

    .text-rose { color: var(--rose); }
    .text-emerald { color: var(--emerald); }
    .text-cyan { color: var(--cyan); }
    .text-amber { color: var(--amber); }

    /* Executive Summary Box */
    .summary-card {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
      border: 1px solid rgba(139, 92, 246, 0.3);
      border-radius: 16px;
      padding: 2rem;
      margin-bottom: 2rem;
    }

    .summary-title {
      font-family: 'Outfit', sans-serif;
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: #c4b5fd;
    }

    .summary-threat {
      display: inline-block;
      padding: 0.4rem 0.8rem;
      background: rgba(244, 63, 94, 0.15);
      border: 1px solid rgba(244, 63, 94, 0.3);
      border-radius: 8px;
      color: #fda4af;
      font-size: 0.9rem;
      font-weight: 600;
      margin-bottom: 1rem;
    }

    .recommendations-list {
      list-style-type: none;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 0.75rem;
    }

    .recommendations-list li {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      padding: 0.75rem 1rem;
      border-radius: 8px;
      font-size: 0.85rem;
      display: flex;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .recommendations-list li::before {
      content: "🛡️";
      font-size: 0.9rem;
    }

    /* Anomaly Breakdown Cards */
    .breakdown-title {
      font-family: 'Outfit', sans-serif;
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.25rem;
    }

    .breakdown-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.25rem;
      margin-bottom: 3rem;
    }

    .breakdown-item {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.25rem;
      position: relative;
    }

    .breakdown-item-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }

    .breakdown-item-name {
      font-weight: 600;
      font-size: 0.95rem;
    }

    .badge-severity {
      font-size: 0.7rem;
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      font-weight: 700;
      text-transform: uppercase;
    }

    .severity-CRITICAL {
      background: rgba(244, 63, 94, 0.15);
      color: var(--rose);
      border: 1px solid rgba(244, 63, 94, 0.3);
    }

    .severity-WARNING {
      background: rgba(245, 158, 11, 0.15);
      color: var(--amber);
      border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .severity-MINOR {
      background: rgba(6, 182, 212, 0.15);
      color: var(--cyan);
      border: 1px solid rgba(6, 182, 212, 0.3);
    }

    .breakdown-count {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.4rem;
      font-weight: 700;
      margin-bottom: 0.25rem;
    }

    .breakdown-impact {
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    /* Remediation Action Bar */
    .remediation-section {
      background: var(--card-bg);
      border: 1px solid rgba(6, 182, 212, 0.3);
      border-radius: 16px;
      padding: 2rem;
      box-shadow: 0 0 35px rgba(6, 182, 212, 0.1);
    }

    .remediation-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1.5rem;
      margin-bottom: 1.5rem;
    }

    .remediation-heading {
      font-family: 'Outfit', sans-serif;
      font-size: 1.35rem;
      font-weight: 700;
    }

    .remediation-sub {
      color: var(--text-muted);
      font-size: 0.9rem;
    }

    .remediation-rules {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .rule-checkbox {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 0.85rem;
      cursor: pointer;
    }

    .rule-checkbox input {
      accent-color: var(--cyan);
      width: 16px;
      height: 16px;
    }

    .btn-download {
      background: linear-gradient(135deg, var(--emerald), #059669);
      color: #fff;
      border: none;
      padding: 0.9rem 2rem;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
    }

    .btn-download:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(16, 185, 129, 0.5);
    }

    /* Loading Spinner */
    .spinner {
      display: none;
      width: 40px;
      height: 40px;
      border: 4px solid rgba(255, 255, 255, 0.1);
      border-left-color: var(--cyan);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      margin: 1.5rem auto;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    /* Toast Notification */
    #toast {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: #1e293b;
      border: 1px solid var(--emerald);
      color: #fff;
      padding: 1rem 1.5rem;
      border-radius: 10px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      display: none;
      z-index: 1000;
      animation: slideUp 0.3s ease;
    }

    @keyframes slideUp {
      from { transform: translateY(50px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <header>
    <div class="nav-container">
      <a href="/" class="brand">
        <div class="brand-icon">⚡</div>
        <div>
          <div class="brand-title">CRM Forensic Audit</div>
          <div class="brand-subtitle">Enterprise Data Remediation</div>
        </div>
      </a>
      <div class="nav-actions">
        <span class="badge-live">Engine Latency: &lt; 150ms</span>
        <a href="/docs" target="_blank" class="btn-secondary">Interactive Swagger API (/docs) ↗</a>
      </div>
    </div>
  </header>

  <main>
    <!-- Hero Section -->
    <section class="hero">
      <h1>Enterprise CRM Forensic Audit &amp; Data Hygiene Microservice</h1>
      <p>Instant in-memory pipeline forensic auditing. Quantify corrupted deals, calculate your enterprise Data Health Score, and stream production-ready datasets.</p>
    </section>

    <!-- Upload & Quick Action Area -->
    <section class="upload-container" id="drop-area">
      <div class="upload-icon">📂</div>
      <div class="upload-title">Ingest Messy Enterprise CRM Export</div>
      <div class="upload-desc">Drag and drop your raw Salesforce or HubSpot CSV file (e.g. <code>crm_deals_dirty.csv</code>)</div>
      
      <input type="file" id="file-input" accept=".csv" style="display: none;">
      
      <div>
        <button class="btn-primary" onclick="document.getElementById('file-input').click()">
          <span>📤 Upload CSV File</span>
        </button>
        <button class="sample-btn" id="btn-load-sample" onclick="loadSampleData()">
          <span>⚡ 1-Click Load 10,000 Dirty Deals</span>
        </button>
      </div>

      <div class="spinner" id="spinner"></div>
    </section>

    <!-- Dashboard Results -->
    <section id="dashboard-results">
      <!-- High-Level KPIs -->
      <div class="kpi-grid">
        <!-- Circular Health Score -->
        <div class="score-card">
          <div class="score-ring">
            <svg>
              <circle class="bg" cx="85" cy="85" r="70"></circle>
              <circle class="progress" id="score-circle" cx="85" cy="85" r="70"></circle>
            </svg>
            <div class="score-text" id="score-val">0.0%</div>
          </div>
          <div class="score-label">Data Health Score</div>
          <div class="score-classification" id="score-class">Analyzing...</div>
        </div>

        <!-- 4 Metric Cards -->
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-title">Revenue At Risk</span>
              <span class="metric-icon">🚨</span>
            </div>
            <div class="metric-value text-rose" id="val-risk">$0.00</div>
            <div class="metric-footer" id="val-risk-pct">0.0% of total pipeline compromised</div>
          </div>

          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-title">Total Pipeline Value</span>
              <span class="metric-icon">💼</span>
            </div>
            <div class="metric-value text-cyan" id="val-pipeline">$0.00</div>
            <div class="metric-footer" id="val-records">From 0 deal records</div>
          </div>

          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-title">Corrupted Deals Detected</span>
              <span class="metric-icon">⚠️</span>
            </div>
            <div class="metric-value text-amber" id="val-corrupted">0</div>
            <div class="metric-footer" id="val-critical-count">0 critical violations found</div>
          </div>

          <div class="metric-card">
            <div class="metric-header">
              <span class="metric-title">Audit Processing Latency</span>
              <span class="metric-icon">⚡</span>
            </div>
            <div class="metric-value text-emerald" id="val-latency">0ms</div>
            <div class="metric-footer">Vectorized Pandas In-Memory Engine</div>
          </div>
        </div>
      </div>

      <!-- Executive Summary Box -->
      <div class="summary-card">
        <div class="summary-title">
          <span>Executive Intelligence &amp; Pipeline Remediation Recommendations</span>
        </div>
        <div class="summary-threat" id="summary-threat">Primary Threat: Initializing...</div>
        <ul class="recommendations-list" id="recommendations-container">
          <!-- Populated by JavaScript -->
        </ul>
      </div>

      <!-- Granular Anomaly Breakdown -->
      <h2 class="breakdown-title">Forensic Anomaly Breakdown</h2>
      <div class="breakdown-grid" id="breakdown-container">
        <!-- Populated by JavaScript -->
      </div>

      <!-- Remediation & Streaming Download Section -->
      <div class="remediation-section">
        <div class="remediation-header">
          <div>
            <div class="remediation-heading">⚡ Automated In-Memory Data Remediation Pipeline</div>
            <div class="remediation-sub">Select rules and stream back a sanitized, production-ready dataset in real-time.</div>
          </div>
          <button class="btn-download" id="btn-remediate" onclick="executeRemediation()">
            <span>🚀 Run Remediation &amp; Stream Clean CSV</span>
          </button>
        </div>

        <div class="remediation-rules">
          <label class="rule-checkbox">
            <input type="checkbox" id="rule-dedup" checked>
            <span>Deduplicate Pipeline (Keep First)</span>
          </label>
          <label class="rule-checkbox">
            <input type="checkbox" id="rule-impute" checked>
            <span>Impute Amounts (Cohort Median)</span>
          </label>
          <label class="rule-checkbox">
            <input type="checkbox" id="rule-email" checked>
            <span>Sanitize RFC Email Syntax</span>
          </label>
          <label class="rule-checkbox">
            <input type="checkbox" id="rule-phone" checked>
            <span>Normalize Phones to E.164</span>
          </label>
          <label class="rule-checkbox">
            <input type="checkbox" id="rule-date" checked>
            <span>Standardize Dates (ISO-8601)</span>
          </label>
          <label class="rule-checkbox">
            <input type="checkbox" id="rule-owner" checked>
            <span>Route Orphan Deals to Ops Pool</span>
          </label>
        </div>
      </div>
    </section>
  </main>

  <div id="toast"></div>

  <script>
    let currentUploadedFile = null;

    // Drag and drop handlers
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');

    ['dragenter', 'dragover'].forEach(name => {
      dropArea.addEventListener(name, (e) => {
        e.preventDefault();
        dropArea.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(name => {
      dropArea.addEventListener(name, (e) => {
        e.preventDefault();
        dropArea.classList.remove('dragover');
      });
    });

    dropArea.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length) handleFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length) handleFile(e.target.files[0]);
    });

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.style.display = 'block';
      setTimeout(() => { toast.style.display = 'none'; }, 4000);
    }

    async function handleFile(file) {
      currentUploadedFile = file;
      const formData = new FormData();
      formData.append('file', file);
      await runAudit(formData);
    }

    async function loadSampleData() {
      const spinner = document.getElementById('spinner');
      spinner.style.display = 'block';
      try {
        const response = await fetch('/api/v1/sample-data');
        if (!response.ok) throw new Error('Could not fetch sample dataset');
        const blob = await response.blob();
        currentUploadedFile = new File([blob], 'crm_deals_dirty.csv', { type: 'text/csv' });
        const formData = new FormData();
        formData.append('file', currentUploadedFile);
        await runAudit(formData);
      } catch (err) {
        alert('Error loading sample data: ' + err.message);
      } finally {
        spinner.style.display = 'none';
      }
    }

    async function runAudit(formData) {
      const spinner = document.getElementById('spinner');
      spinner.style.display = 'block';
      try {
        const res = await fetch('/api/v1/audit', {
          method: 'POST',
          body: formData
        });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Audit failed');
        }
        const data = await res.json();
        renderAuditReport(data);
        showToast('Forensic Audit completed in ' + data.execution_time_ms + 'ms!');
      } catch (err) {
        alert('Audit Error: ' + err.message);
      } finally {
        spinner.style.display = 'none';
      }
    }

    function renderAuditReport(data) {
      document.getElementById('dashboard-results').style.display = 'block';

      // Score Ring
      const score = data.hygiene_score;
      document.getElementById('score-val').innerText = score.toFixed(1) + '%';
      document.getElementById('score-class').innerText = data.executive_summary.health_classification;
      
      const circumference = 440;
      const offset = circumference - (score / 100) * circumference;
      document.getElementById('score-circle').style.strokeDashoffset = offset;

      // Color coding for score
      const circle = document.getElementById('score-circle');
      if (score >= 90) circle.style.stroke = '#10b981';
      else if (score >= 70) circle.style.stroke = '#06b6d4';
      else if (score >= 50) circle.style.stroke = '#f59e0b';
      else circle.style.stroke = '#f43f5e';

      // KPI Metrics
      document.getElementById('val-risk').innerText = '$' + Number(data.revenue_at_risk).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
      document.getElementById('val-risk-pct').innerText = data.risk_percentage + '% of pipeline dollars compromised';

      document.getElementById('val-pipeline').innerText = '$' + Number(data.total_pipeline_value).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
      document.getElementById('val-records').innerText = 'From ' + data.total_records.toLocaleString() + ' total records ingested';

      document.getElementById('val-corrupted').innerText = data.corrupted_records.toLocaleString();
      document.getElementById('val-critical-count').innerText = data.anomalies_by_severity.CRITICAL.toLocaleString() + ' critical business violations';

      document.getElementById('val-latency').innerText = data.execution_time_ms + 'ms';

      // Executive Summary
      document.getElementById('summary-threat').innerText = '⚠️ Primary Revenue Threat: ' + data.executive_summary.primary_revenue_threat;
      const recContainer = document.getElementById('recommendations-container');
      recContainer.innerHTML = '';
      data.executive_summary.actionable_recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.innerText = rec;
        recContainer.appendChild(li);
      });

      // Anomaly Breakdown Grid
      const bContainer = document.getElementById('breakdown-container');
      bContainer.innerHTML = '';

      const items = [
        { name: 'Duplicate Deals', detail: data.anomaly_breakdown.duplicate_deals },
        { name: 'Invalid / Negative Amounts', detail: data.anomaly_breakdown.invalid_amounts },
        { name: 'Expired Stages & Zombie Deals', detail: data.anomaly_breakdown.stage_mismatches },
        { name: 'Malformed Emails', detail: data.anomaly_breakdown.malformed_emails },
        { name: 'Malformed Phone Numbers', detail: data.anomaly_breakdown.malformed_phones },
        { name: 'Unassigned Account Owners', detail: data.anomaly_breakdown.unassigned_owners },
        { name: 'Corrupted UTF-8 Encodings', detail: data.anomaly_breakdown.corrupted_encodings },
        { name: 'Non-Standard Dates', detail: data.anomaly_breakdown.non_standard_dates },
      ];

      items.forEach(item => {
        const div = document.createElement('div');
        div.className = 'breakdown-item';
        div.innerHTML = `
          <div class="breakdown-item-top">
            <span class="breakdown-item-name">${item.name}</span>
            <span class="badge-severity severity-${item.detail.severity}">${item.detail.severity}</span>
          </div>
          <div class="breakdown-count">${item.detail.count.toLocaleString()}</div>
          <div class="breakdown-impact">
            ${item.detail.monetary_impact_usd > 0 ? 'Financial Impact: $' + Number(item.detail.monetary_impact_usd).toLocaleString() : 'Data Integrity & Routing Failure'}
          </div>
        `;
        bContainer.appendChild(div);
      });

      // Smooth scroll to results
      document.getElementById('dashboard-results').scrollIntoView({ behavior: 'smooth' });
    }

    async function executeRemediation() {
      if (!currentUploadedFile) {
        alert('Please upload or load a CRM dataset first.');
        return;
      }

      const btn = document.getElementById('btn-remediate');
      btn.innerHTML = '<span>⏳ Processing Remediation...</span>';
      btn.disabled = true;

      const config = {
        deduplicate: document.getElementById('rule-dedup').checked,
        impute_amounts: document.getElementById('rule-impute').checked,
        imputation_strategy: 'median',
        sanitize_emails: document.getElementById('rule-email').checked,
        normalize_phones: document.getElementById('rule-phone').checked,
        normalize_dates: document.getElementById('rule-date').checked,
        resolve_orphan_owners: document.getElementById('rule-owner').checked,
        fix_encoding: true,
        reconcile_stage_dates: true
      };

      const formData = new FormData();
      formData.append('file', currentUploadedFile);
      formData.append('config', JSON.stringify(config));

      try {
        const response = await fetch('/api/v1/remediate', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) throw new Error('Remediation stream failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'sanitized_crm_deals.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);

        showToast('Sanitized dataset downloaded successfully!');
      } catch (err) {
        alert('Remediation Error: ' + err.message);
      } finally {
        btn.innerHTML = '<span>🚀 Run Remediation &amp; Stream Clean CSV</span>';
        btn.disabled = false;
      }
    }
  </script>
</body>
</html>
"""
