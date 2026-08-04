"""
Refactored, Highly Reliable Playwright Test Suite for Part 1
File: tests/test_part1_debugging.py
Candidate: Vivek Bukka
"""

import os
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

BASE_URL = os.getenv("BASE_URL", "https://app.workflowpro.com")
DEFAULT_TIMEOUT = 15000  # 15s timeout for CI stability


@pytest.mark.smoke
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_user_login(page: Page):
    """
    Part 1 Fix: Validates user login functionality with web-first assertions.
    Fixes URL race condition, 2FA prompts, and element visibility flakiness.
    """
    # 1. Set standard desktop viewport to avoid responsive layout shifts
    page.set_viewport_size({"width": 1920, "height": 1080})

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    # 2. Navigate with network idle waiting strategy
    login_page.navigate_to(f"{BASE_URL}/login")

    # 3. Fill login form and submit (handles 2FA contextually)
    login_page.login(email="admin@company1.com", password="password123")

    # 4. FIX 1: Web-first URL assertion auto-waits for route transition
    login_page.wait_for_url_match(f"{BASE_URL}/dashboard", timeout=DEFAULT_TIMEOUT)

    # 5. FIX 2: Web-first element assertion auto-waits for DOM presence & visibility
    dashboard_page.verify_welcome_message(expected_text="Welcome", timeout=DEFAULT_TIMEOUT)


@pytest.mark.tenant
def test_multi_tenant_access(page: Page):
    """
    Part 1 Fix: Validates multi-tenant data isolation for Company 2.
    Fixes immediate list evaluation flakiness (.all()) by using locator count expectations.
    """
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.navigate_to(f"{BASE_URL}/login")
    login_page.login(email="user@company2.com", password="password123")

    # Wait for dashboard transition
    login_page.wait_for_url_match(f"{BASE_URL}/dashboard", timeout=DEFAULT_TIMEOUT)

    # FIX 3: Wait for project cards locator to finish dynamic API loading before evaluating
    project_cards = dashboard_page.project_cards
    expect(project_cards.first).to_be_visible(timeout=DEFAULT_TIMEOUT)

    card_count = project_cards.count()
    assert card_count > 0, "Expected at least one project card for Company2"

    for i in range(card_count):
        card = project_cards.nth(i)
        expect(card).to_contain_text("Company2")
