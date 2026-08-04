# 🧪 WorkFlow Pro — B2B SaaS Multi-Platform Test Automation Framework

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.41-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.3-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![BrowserStack](https://img.shields.io/badge/BrowserStack-Supported-FF6F00?style=for-the-badge&logo=browserstack&logoColor=white)
![CI/CD Pipeline](https://img.shields.io/badge/GitHub_Actions-Passed-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

**Candidate Name:** Vivek Bukka  
**Role:** Automation Engineering Intern  
**Company:** Bynry Inc. · Wai (Hybrid)  
**Submission Date:** August 4, 2026  
**Repository URL:** [https://github.com/bvivek2148/Vivek-Bukka-QA-Automation-Engineering-Case-Study](https://github.com/bvivek2148/Vivek-Bukka-QA-Automation-Engineering-Case-Study)  

---

## 📌 Executive Summary & Submission Artifacts

This repository contains the complete production-ready test automation framework and solution for the **WorkFlow Pro B2B SaaS Platform** QA Automation Case Study.

- 📄 **Technical Case Study Solution:** 
  - Markdown Version: [CASE_STUDY_SOLUTION.md](./CASE_STUDY_SOLUTION.md)
  - Word Document Version: [docs/CASE_STUDY_SOLUTION.docx](./docs/CASE_STUDY_SOLUTION.docx)
- 📋 **Master Test Plan:** 
  - Markdown Version: [TEST_PLAN.md](./TEST_PLAN.md)
  - Word Document Version: [docs/TEST_PLAN.docx](./docs/TEST_PLAN.docx)
- 📊 **HTML Execution Report:** [reports/report.html](./reports/report.html)

---

## 🏗️ Repository Architecture & Directory Structure

The framework uses **Python 3.12**, **Pytest**, **Playwright**, **Page Object Model (POM)**, and **Pydantic configuration management**:

```
Vivek-Bukka-QA-Automation-Engineering-Case-Study/
├── .github/
│   └── workflows/
│       └── regression.yml          # GitHub Actions CI/CD Regression Workflow
├── config/
│   ├── __init__.py
│   ├── config.py                   # Dynamic Pydantic Configuration Loader
│   └── environments.yaml           # Multi-tenant URLs, API Gateways, & Credentials
├── docs/                           # Formatted Microsoft Word (.docx) Documentation
│   ├── CASE_STUDY_SOLUTION.docx    # Formatted Case Study Solution (Word)
│   ├── TEST_PLAN.docx              # Formatted Master Test Plan (Word)
│   └── QA Automation Engineering Case Study.docx # Original Case Study Prompt Document
├── pages/                          # Page Object Model (POM)
│   ├── __init__.py
│   ├── base_page.py                # Base Page with Web-First Auto-Waits & Assertions
│   ├── login_page.py               # Login UI Selectors & Authentication Workflows
│   └── dashboard_page.py           # Dashboard & Project Components
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest Fixtures (API Client, Session State, Light Report Hooks)
│   ├── test_part1_debugging.py     # Part 1 Debugging Suite (Flakiness & Race Condition Fixes)
│   └── test_part3_integration.py   # Part 3 Hybrid API + Web UI + Mobile + Security Test
├── reports/
│   ├── README.md                   # HTML Reports Execution Guide
│   └── report.html                 # Self-Contained Professional Light HTML Execution Report
├── build_perfect_docx.py           # Markdown-to-DOCX Formatting Utility
├── CASE_STUDY_SOLUTION.md          # Complete Master Case Study Technical Submission Document
├── TEST_PLAN.md                    # Dedicated Master Test Plan & Risk Strategy Document
├── pytest.ini                      # Pytest Configuration (Pythonpath, CLI Flags, Markers)
├── requirements.txt                # Python Dependencies
└── README.md                       # Main Repository Documentation Guide
```

---

## 🚀 Key Framework Capabilities

1. **Flaky Test Immunity (Part 1 Solution):**
   * Replaces raw assertions with Playwright's **web-first assertions** (`expect(page).to_have_url()`, `expect(locator).to_be_visible()`).
   * Fixes immediate list evaluation bugs (`.all()`) by enforcing dynamic element count locator expectations (`expect(project_cards.first).to_be_visible()`).

2. **Modular Architecture & Multi-Tenant Routing (Part 2 Solution):**
   * **Page Object Model (POM)** isolates selector definitions from test logic for clean maintainability.
   * **Dynamic Environment Loader (`config/config.py`):** Configures multi-tenant subdomains (`company1.workflowpro.com`, `company2.workflowpro.com`).
   * **Session Storage Caching:** Reuses `storage_state.json` to bypass UI login overhead across test runs.

3. **End-to-End Hybrid Integration Testing (Part 3 Solution):**
   * **API Layer:** Creates test projects via `POST /api/v1/projects` using `api_client` fixture.
   * **Web UI Layer:** Validates project rendering on desktop viewports.
   * **Mobile UI Layer:** Validates mobile responsive viewports (`390x844` iPhone 14 specs) & handles hamburger navigation menus.
   * **Tenant Isolation Security Boundary:** Logs in as an unprivileged tenant (`Company 2`) and asserts that `Company 1` data is invisible.
   * **Automated Data Teardown:** Pytest `yield` hooks automatically issue `DELETE` calls post-test to maintain database hygiene.

---

## 🛠️ Setup & Local Execution Guide

### 1. Clone Repository & Install Dependencies

```bash
# Clone repository
git clone https://github.com/bvivek2148/Vivek-Bukka-QA-Automation-Engineering-Case-Study.git
cd Vivek-Bukka-QA-Automation-Engineering-Case-Study

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
python -m playwright install chromium
```

### 2. Running Test Suites & HTML Report Generation

```bash
# Run all test suites (Parts 1 & 3)
python -m pytest

# Run Part 1 Debugging tests only
python -m pytest tests/test_part1_debugging.py

# Run Part 3 Integration tests only
python -m pytest tests/test_part3_integration.py

# Verify test discovery and collection without execution
python -m pytest --collect-only

# Generate self-contained Light Theme HTML report
python -m pytest --html=reports/report.html --self-contained-html
```

---

## 📊 Sample Test Execution Output

```text
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-8.3.5, pluggy-1.5.0
rootdir: D:\Delete folder-C\web develpment\New folder\New folder\Vivek-Bukka QA Automation Case Study
configfile: pytest.ini
collected 3 items

tests/test_part1_debugging.py::test_user_login[chromium] PASSED
tests/test_part1_debugging.py::test_multi_tenant_access[chromium] PASSED
tests/test_part3_integration.py::test_project_creation_flow[chromium] PASSED

============================== 3 passed in 7.06s ==============================
```

---

## ⚙️ CI/CD Pipeline Integration

The repository includes an automated GitHub Actions pipeline (`.github/workflows/regression.yml`) configured to:
- Automatically trigger on `push` to `main` and on `pull_request`.
- Execute automated Playwright test collection and regression runs on Ubuntu runners.
- Upload HTML execution reports as build artifacts for full team visibility.

---

*Authored by Vivek Bukka for Bynry Inc. QA Automation Engineering Intern Assessment.*
