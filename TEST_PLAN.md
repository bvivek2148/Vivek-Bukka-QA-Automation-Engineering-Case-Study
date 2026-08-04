# 📋 Master Test Plan & QA Automation Strategy — WorkFlow Pro B2B SaaS Platform

**Candidate Name:** Vivek Bukka  
**Target Role:** Automation Engineering Intern  
**Company:** Bynry Inc. · Wai (Hybrid)  
**Document Version:** 1.0 (Final Production Submission)  
**Submission Date:** August 4, 2026  
**Repository URL:** [https://github.com/bvivek2148/Vivek-Bukka-QA-Automation-Engineering-Case-Study](https://github.com/bvivek2148/Vivek-Bukka-QA-Automation-Engineering-Case-Study)  

---

## 1. Executive Summary & Objectives

This **Master Test Plan** defines the end-to-end quality assurance and test automation strategy for the **WorkFlow Pro B2B SaaS Platform**. WorkFlow Pro is a multi-tenant enterprise platform that enables organizations (`Company 1`, `Company 2`, etc.) to manage projects, teams, and workflows with strict tenant data isolation.

### 1.1 Core QA Objectives
1. **Flaky Test Elimination (Part 1):** Debug and refactor intern-authored Playwright scripts by replacing raw assertions with web-first auto-waiting assertions and enforcing dynamic element count expectations.
2. **Framework Architecture & Scalability (Part 2):** Design a modular Page Object Model (POM) test framework leveraging Python 3.12, Pytest, Playwright, Pydantic configuration management, and BrowserStack cross-platform execution.
3. **End-to-End Hybrid Integration (Part 3):** Validate full business scenarios combining REST API project creation (`POST /api/v1/projects`), Web UI dashboard rendering, Mobile responsive viewport accessibility (`390x844`), and negative security tenant isolation.

---

## 2. Test Scope & Exclusions

### 2.1 In-Scope Functional & Technical Areas
- **Web UI Authentication:** Single-Factor Login, 2FA contextual prompt handling, and session storage caching (`storage_state.json`).
- **Multi-Tenant Isolation:** Validating positive access boundaries for `Company 1` users and enforcing negative data visibility boundaries for `Company 2` users.
- **REST API Automation:** HTTP request payload validation, status code checks, Bearer token authentication, `X-Tenant-ID` header handling, and post-test teardown hooks (`DELETE /api/v1/projects/{id}`).
- **Mobile Responsive Viewports:** Viewport scaling (`iPhone 14` specs) and mobile navigation menu interactions.
- **CI/CD Pipeline:** Automated headless test execution and artifact generation via GitHub Actions (`.github/workflows/regression.yml`).

### 2.2 Out-of-Scope Areas
- Non-functional load/stress testing exceeding SLA timeouts (15s).
- Destructive database migrations or production data purging.

---

## 3. High-Level Automation Architecture

```text
                               ┌──────────────────────────────────┐
                               │  Pytest Test Runner (pytest.ini) │
                               └────────────────┬─────────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
    ┌─────────────────────────┐    ┌─────────────────────────┐    ┌─────────────────────────┐
    │     API Client Layer    │    │     Web & Mobile UI     │    │   Tenant Security Layer │
    │   POST /api/v1/projects │    │  Playwright POM (Web)   │    │  Negative Access Checks │
    │    DELETE Teardown Hook │    │  iPhone Viewport (Mob)  │    │  (Company1 vs Company2) │
    └─────────────────────────┘    └─────────────────────────┘    └─────────────────────────┘
                                                │
                                                ▼
                               ┌──────────────────────────────────┐
                               │  Reports Layer (reports/report.html)│
                               └──────────────────────────────────┘
```

### 3.1 Framework Layer Responsibilities
- **Config Manager (`config/config.py` & `config/environments.yaml`):** Loads tenant subdomains, API gateways, and user role credentials.
- **Base Page Object (`pages/base_page.py`):** Encapsulates core Playwright actions with web-first auto-waits (`navigate_to`, `wait_for_url_match`).
- **Page Objects (`pages/login_page.py`, `pages/dashboard_page.py`):** Isolates DOM selectors from test assertions for maximum reusability.
- **Fixtures & Hooks (`tests/conftest.py`):** Handles Playwright browser context initialization, SSL cert error overrides, mock route interception, API client fixtures, teardown hooks, and light-theme HTML report styling.

---

## 4. Requirements Traceability & Test Scenarios Matrix

| Scenario ID | Test Scenario Name | Layer | Target Component | Expected Outcome | Execution Status |
|---|---|---|---|---|---|
| **TS-01** | User Login & 2FA Validation | Web UI | `LoginPage` | Navigates to `/login`, fills credentials, handles 2FA contextually, and auto-waits for `/dashboard`. | ✅ **PASSED** (2.77s) |
| **TS-02** | Multi-Tenant Card Loading | Web UI | `DashboardPage` | Logs in as `Company 2`, waits for dynamic locator count (`project_cards.first`), and asserts tenant card labels. | ✅ **PASSED** (0.86s) |
| **TS-03** | Dynamic Config Loading | Framework | `config.py` | Reads `environments.yaml` using Pydantic models for `staging` & `prod` environments. | ✅ **PASSED** |
| **TS-04** | Role Auth Session Storage | Framework | `conftest.py` | Saves `admin_state.json` once per session to bypass UI login overhead on repetitive tests. | ✅ **PASSED** |
| **TS-05** | E2E Hybrid Project Creation Flow | API + Web + Mobile + Security | Integration | 1. API: `POST /api/v1/projects`<br>2. Web UI: Verify card on Company 1 dashboard<br>3. Mobile UI: Verify iPhone 14 responsive menu<br>4. Security: Assert card **invisible** to Company 2<br>5. Teardown: `DELETE /api/v1/projects/{id}` | ✅ **PASSED** (7.06s) |

---

## 5. Test Data Management & Lifecycle Policy

```
[API POST /projects] ──► [Record Project ID] ──► [UI & Mobile Validation] ──► [Pytest Yield Teardown] ──► [API DELETE /projects/{id}]
```

1. **Collision Prevention:** Uses dynamic project names (`Auto_Test_Project_{os.urandom(4).hex()}`) to ensure zero data collisions during parallel or rerun executions.
2. **Multi-Tenant Credentials:** Managed via `config/environments.yaml` for `Company 1` (`admin@company1.com`) and `Company 2` (`user@company2.com`).
3. **Automated Resource Purging:** Pytest `api_client` fixture uses `yield` blocks to automatically execute `DELETE /api/v1/projects/{id}` post-test.

---

## 6. Environment & Cross-Platform Capability Matrix

| Platform / Layer | Execution Engine | Viewport / Device Specs | Strategy |
|---|---|---|---|
| **Web UI (Desktop)** | Chromium (Playwright) | `1920x1080` Viewport | Local headless execution with Playwright web-first assertions. |
| **Mobile UI (Local)** | Chromium Mobile Emulation | `390x844` (iPhone 14) | Viewport scaling & mobile hamburger menu navigation during PR builds. |
| **Mobile UI (Cloud)** | BrowserStack W3C Remote | Real iOS (Safari) / Android | Triggered via BrowserStack cloud capabilities during Nightly Regression runs. |
| **API Backend** | Python `requests` HTTP Client | REST JSON API Gateways | Direct HTTP calls with Bearer auth & `X-Tenant-ID` headers. |

---

## 7. Risk Assessment & Mitigation Strategies

| Risk Factor | Severity | Mitigation Strategy |
|---|---|---|
| **Network Latency & Slow CI VMs** | High | Enforced 15s web-first timeouts (`expect().to_be_visible()`) and automatic retries (`reruns=2`). |
| **Data Pollution across Tenants** | High | Dynamic hex project naming + Pytest fixture `yield` teardown hooks. |
| **SSL Certificate Errors in Staging** | Medium | Configured `ignore_https_errors=True` in `conftest.py`. |
| **BrowserStack Quota & Cost Limits** | Medium | Restrict real BrowserStack device runs to Nightly builds; use local emulators for PRs. |

---

## 8. Defect Criteria & Entry/Exit Governance

### 8.1 Entry Criteria
- Staging environment (`staging.workflowpro.com`) is deployed and accessible.
- API gateway endpoints (`/api/v1/projects`) return valid HTTP status responses.
- Test runner environment has Python 3.12+ and Playwright Chromium binaries installed.

### 8.2 Exit Criteria
- **100% Pass Rate** across all automated test suites (`test_part1_debugging.py` and `test_part3_integration.py`).
- Zero P0/P1 blocking defects open.
- Self-contained HTML report (`reports/report.html`) generated and attached to CI pipeline artifacts.

---

## 9. Local Execution & CI/CD Pipeline Automation

### 9.1 Local Test Execution Commands
```bash
# Run full test suite with HTML report generation
python -m pytest --html=reports/report.html --self-contained-html

# Run Part 1 Debugging tests
python -m pytest tests/test_part1_debugging.py

# Run Part 3 E2E Integration tests
python -m pytest tests/test_part3_integration.py
```

### 9.2 GitHub Actions CI/CD Pipeline (`.github/workflows/regression.yml`)
- Triggers on every `push` to `main` branch and on `pull_request`.
- Executes headless Playwright test suites on Ubuntu runners.
- Uploads `reports/report.html` as build artifacts.

---

*Master Test Plan — Authored by Vivek Bukka for Bynry Inc. QA Automation Engineering Assessment.*
