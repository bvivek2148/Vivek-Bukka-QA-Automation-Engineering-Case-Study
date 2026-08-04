"""
End-to-End API + UI + Mobile + Security Integration Test
File: tests/test_part3_integration.py
Candidate: Vivek Bukka
"""

import os
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

WEB_BASE_URL = os.getenv("WEB_BASE_URL", "https://app.workflowpro.com")


@pytest.mark.integration
def test_project_creation_flow(page: Page, api_client):
    """
    Business Scenario Validation:
    1. API: Create project via POST /api/v1/projects (with Tenant-ID & Bearer token).
    2. Web UI: Verify created project renders correctly on Company 1 Web dashboard.
    3. Mobile UI: Verify project accessibility on mobile viewport / BrowserStack emulation.
    4. Security Isolation: Log in as Company 2 user and verify negative security boundary.
    
    Testing Strategy & Edge Cases Handled:
    - Test Data Isolation: Uses dynamic UUIDs/hex strings to prevent data collisions.
    - Automated Cleanup: api_client fixture uses yield hooks to purge test data post-test.
    - Flakiness Resilience: Web-first assertions (expect().to_be_visible()) handle network latency.
    - Cross-Platform & Responsive: Simulates iPhone 14 viewport and handles mobile burger menus.
    """
    tenant_company1 = "company1-uuid"
    tenant_company2 = "company2-uuid"
    project_name = f"Auto_Test_Project_{os.urandom(4).hex()}"
    
    # -------------------------------------------------------------------------
    # STEP 1: API - Create Project
    # Endpoint: POST /api/v1/projects
    # Headers: Authorization: Bearer {token}, X-Tenant-ID: {company_id}
    # -------------------------------------------------------------------------
    project = api_client(
        tenant_id=tenant_company1,
        name=project_name,
        description="E2E Integration Test Project"
    )
    assert project["name"] == project_name
    assert project["status"] == "active"

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    # -------------------------------------------------------------------------
    # STEP 2: Web UI - Verify Project Display for Company 1 User
    # Validates backend API creation reflects immediately in frontend DOM.
    # -------------------------------------------------------------------------
    login_page.navigate_to(f"{WEB_BASE_URL}/login")
    login_page.login(email="admin@company1.com", password="password123")
    login_page.wait_for_url_match(f"{WEB_BASE_URL}/dashboard")
    
    dashboard_page.verify_project_exists(project_name=project_name)

    # -------------------------------------------------------------------------
    # STEP 3: Mobile UI - Check Mobile Accessibility & Responsive View
    # Simulates iPhone 14 responsive viewport (390x844) & handles mobile burger menu.
    # On BrowserStack CI runs, this connects via BrowserStack W3C remote capabilities.
    # -------------------------------------------------------------------------
    page.set_viewport_size({"width": 390, "height": 844})
    dashboard_page.open_mobile_menu_if_present()
    dashboard_page.verify_project_exists(project_name=project_name)

    # -------------------------------------------------------------------------
    # STEP 4: Security - Validate Tenant Isolation (Company 2 User)
    # Negative Security Boundary Assertion: Ensures Company 2 CANNOT view Company 1 data.
    # -------------------------------------------------------------------------
    login_page.navigate_to(f"{WEB_BASE_URL}/login")
    login_page.login(email="user@company2.com", password="password123")
    login_page.wait_for_url_match(f"{WEB_BASE_URL}/dashboard")
    
    dashboard_page.verify_project_not_exists(project_name=project_name)
