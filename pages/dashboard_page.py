from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class DashboardPage(BasePage):
    """Page Object for Dashboard screen."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.welcome_message = page.locator(".welcome-message")
        self.project_cards = page.locator(".project-card")
        self.mobile_menu_btn = page.locator("#mobile-menu-btn")

    def verify_welcome_message(self, expected_text: str = "Welcome back", timeout: int = 15000):
        expect(self.welcome_message).to_be_visible(timeout=timeout)
        expect(self.welcome_message).to_contain_text(expected_text)

    def verify_project_exists(self, project_name: str, timeout: int = 15000):
        card = self.page.locator(f".project-card:has-text('{project_name}')")
        expect(card).to_be_visible(timeout=timeout)
        return card

    def verify_project_not_exists(self, project_name: str, timeout: int = 5000):
        card = self.page.locator(f".project-card:has-text('{project_name}')")
        expect(card).not_to_be_visible(timeout=timeout)

    def open_mobile_menu_if_present(self):
        if self.mobile_menu_btn.is_visible(timeout=3000):
            self.mobile_menu_btn.click()
