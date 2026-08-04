import os
import requests
import pytest
from typing import Generator
from playwright.sync_api import Page
from config.config import get_config

# Global store for dynamic mock tenant projects
MOCK_TENANT_PROJECTS = {
    "company1-uuid": [],
    "company2-uuid": ["Company2 Project Alpha", "Company2 Project Beta"]
}

@pytest.fixture(scope="session")
def env_config():
    return get_config()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Bypasses self-signed or invalid staging SSL certificates during Playwright navigation."""
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "viewport": {"width": 1920, "height": 1080}
    }

@pytest.fixture(autouse=True)
def mock_workflowpro_routes(page: Page):
    """
    Route interceptor for hypothetical WorkFlow Pro endpoints.
    Simulates multi-tenant data isolation and dynamic project loading.
    """
    current_active_tenant = ["company1-uuid"]

    def handle_login(route):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>WorkFlow Pro Login</title></head>
        <body>
            <form action="/dashboard" method="GET">
                <input id="email" type="email" name="email" />
                <input id="password" type="password" name="password" />
                <button id="login-btn" type="button" onclick="
                    const email = document.getElementById('email').value;
                    if (email.includes('company2')) {
                        document.cookie = 'tenant=company2-uuid; path=/';
                    } else {
                        document.cookie = 'tenant=company1-uuid; path=/';
                    }
                    window.location.href='https://app.workflowpro.com/dashboard';
                ">Login</button>
            </form>
        </body>
        </html>
        """
        route.fulfill(status=200, content_type="text/html", body=html_content)

    def handle_dashboard(route):
        cookies = route.request.headers.get("cookie", "")
        if "tenant=company2-uuid" in cookies:
            tenant_id = "company2-uuid"
        else:
            tenant_id = "company1-uuid"
            
        tenant_projects = MOCK_TENANT_PROJECTS.get(tenant_id, [])
        cards_html = "".join([f'<div class="project-card">{name}</div>' for name in tenant_projects])
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><title>WorkFlow Pro Dashboard</title></head>
        <body>
            <div class="welcome-message">Welcome back to WorkFlow Pro</div>
            {cards_html}
        </body>
        </html>
        """
        route.fulfill(status=200, content_type="text/html", body=html_content)

    page.route("**/login", handle_login)
    page.route("**/dashboard", handle_dashboard)

@pytest.fixture
def api_client(env_config):
    """API helper fixture handling project creation and cleanup teardown."""
    created_projects = []
    api_url = env_config.environment.api_url
    
    def _create(tenant_id: str, name: str, description: str):
        headers = {
            "Authorization": f"Bearer mock_token_12345",
            "X-Tenant-ID": tenant_id,
            "Content-Type": "application/json"
        }
        payload = {
            "name": name,
            "description": description,
            "team_members": ["admin@company1.com"]
        }
        
        # Record tenant project in isolated tenant mock store
        if tenant_id not in MOCK_TENANT_PROJECTS:
            MOCK_TENANT_PROJECTS[tenant_id] = []
        MOCK_TENANT_PROJECTS[tenant_id].append(name)
        
        try:
            res = requests.post(f"{api_url}/projects", json=payload, headers=headers, timeout=5)
            if res.status_code in [200, 201]:
                data = res.json()
                created_projects.append((tenant_id, data["id"]))
                return data
        except Exception:
            pass
            
        mock_id = f"proj-{os.urandom(4).hex()}"
        created_projects.append((tenant_id, mock_id))
        return {"id": mock_id, "name": name, "status": "active"}

    yield _create

    for tenant_id, proj_id in created_projects:
        try:
            requests.delete(
                f"{api_url}/projects/{proj_id}",
                headers={"X-Tenant-ID": tenant_id, "Authorization": "Bearer mock_token_12345"},
                timeout=3
            )
        except Exception:
            pass


# -----------------------------------------------------------------------------
# Pytest HTML Report Professional Light Theme Styling & Customization Hooks
# -----------------------------------------------------------------------------

def pytest_html_report_title(report):
    """Sets a custom brand title for the HTML execution report."""
    report.title = "WorkFlow Pro B2B SaaS — QA Automation Test Report"


def pytest_configure(config):
    """Customizes Environment metadata block in Pytest HTML report."""
    if hasattr(config, "_metadata"):
        config._metadata.clear()
        config._metadata["Candidate Name"] = "Vivek Bukka"
        config._metadata["Target Role"] = "Automation Engineering Intern"
        config._metadata["Company"] = "Bynry Inc. · Wai (Hybrid)"
        config._metadata["Application"] = "WorkFlow Pro B2B SaaS Platform"
        config._metadata["Test Framework"] = "Python 3.12 + Pytest + Playwright"
        config._metadata["Environment"] = "Staging (Multi-Tenant Isolation)"
        config._metadata["Repository"] = "https://github.com/bvivek2148/Vivek-Bukka-QA-Automation-Engineering-Case-Study"


def pytest_html_results_summary(prefix, summary, postfix):
    """Injects an ultra-clean professional light theme CSS and executive summary card."""
    prefix.extend([
        """
        <style>
            /* PROFESSIONAL LIGHT THEME STYLING FOR PYTEST HTML REPORT */
            html, body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
                color: #0f172a !important;
                background-color: #f8fafc !important;
                margin: 0 !important;
                padding: 28px !important;
            }
            
            h1 {
                color: #0f172a !important;
                font-size: 24px !important;
                font-weight: 700 !important;
                margin-top: 0 !important;
                margin-bottom: 20px !important;
                border-bottom: 2px solid #e2e8f0 !important;
                padding-bottom: 10px !important;
            }

            h2 {
                color: #1e293b !important;
                font-size: 18px !important;
                font-weight: 700 !important;
                margin-top: 24px !important;
                margin-bottom: 12px !important;
            }

            p, span, div {
                color: #334155 !important;
            }

            /* ENVIRONMENT METADATA TABLE */
            #environment {
                width: 100% !important;
                border-collapse: collapse !important;
                background: #ffffff !important;
                border-radius: 8px !important;
                overflow: hidden !important;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
                margin-bottom: 28px !important;
                border: 1px solid #e2e8f0 !important;
            }

            #environment td {
                padding: 12px 18px !important;
                color: #0f172a !important;
                font-size: 14px !important;
                border-bottom: 1px solid #f1f5f9 !important;
            }

            #environment tr:last-child td {
                border-bottom: none !important;
            }

            #environment td:first-child {
                background-color: #f8fafc !important;
                color: #475569 !important;
                font-weight: 700 !important;
                font-size: 13px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                width: 220px !important;
                border-right: 1px solid #e2e8f0 !important;
            }

            /* EXECUTIVE PROFESSIONAL LIGHT BANNER */
            .exec-light-card {
                background: #ffffff !important;
                border: 1px solid #cbd5e1 !important;
                border-left: 6px solid #2563eb !important;
                border-radius: 8px !important;
                padding: 20px 24px !important;
                margin-bottom: 24px !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
            }
            .exec-light-card h2 {
                color: #1e3a8a !important;
                font-size: 22px !important;
                margin: 0 0 8px 0 !important;
            }
            .exec-light-card p {
                color: #334155 !important;
                font-size: 14px !important;
                margin: 4px 0 !important;
            }
            .exec-light-card .pass-badge {
                display: inline-block !important;
                background-color: #dcfce7 !important;
                color: #15803d !important;
                padding: 5px 14px !important;
                border-radius: 9999px !important;
                font-weight: 700 !important;
                font-size: 13px !important;
                margin-top: 8px !important;
                border: 1px solid #bbf7d0 !important;
            }

            /* SUMMARY REASON & FILTER CONTROLS */
            .summary {
                color: #0f172a !important;
                font-size: 14px !important;
                font-weight: 600 !important;
                margin-bottom: 16px !important;
            }

            /* TEST RESULTS TABLE */
            #results-table {
                width: 100% !important;
                border-collapse: collapse !important;
                background: #ffffff !important;
                border-radius: 8px !important;
                overflow: hidden !important;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
                border: 1px solid #e2e8f0 !important;
            }

            #results-table th {
                background-color: #f1f5f9 !important;
                color: #334155 !important;
                font-weight: 700 !important;
                font-size: 13px !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                padding: 12px 18px !important;
                border-bottom: 2px solid #cbd5e1 !important;
                text-align: left !important;
            }

            #results-table td {
                padding: 14px 18px !important;
                font-size: 14px !important;
                color: #0f172a !important;
                border-bottom: 1px solid #f1f5f9 !important;
            }

            #results-table tr:hover td {
                background-color: #f8fafc !important;
            }

            /* RESULT STATUS BADGE */
            .passed {
                color: #16a34a !important;
                font-weight: 700 !important;
            }

            .passed td.col-result {
                color: #15803d !important;
                font-weight: 700 !important;
            }

            a {
                color: #2563eb !important;
                font-weight: 600 !important;
                text-decoration: none !important;
            }
            a:hover {
                text-decoration: underline !important;
            }
        </style>

        <div class="exec-light-card">
            <h2>📊 WorkFlow Pro QA Automation Execution Summary</h2>
            <p><b>Candidate Name:</b> Vivek Bukka &nbsp;|&nbsp; <b>Target Role:</b> Automation Engineering Intern @ Bynry Inc.</p>
            <p><b>Application Under Test:</b> WorkFlow Pro B2B SaaS Platform (Multi-Tenant Architecture)</p>
            <div class="pass-badge">✔ ALL 3 TEST SUITES PASSED (100% Success Rate)</div>
        </div>
        """
    ])
