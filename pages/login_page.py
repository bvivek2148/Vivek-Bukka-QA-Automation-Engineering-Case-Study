from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for WorkFlow Pro Login screen."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-btn")
        self.two_fa_input = page.locator("#two-factor-code")
        self.verify_2fa_btn = page.locator("#verify-2fa-btn")

    def login(self, email: str, password: str, secret_2fa: str = None):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        
        # Contextually handle 2FA if prompt appears
        if self.two_fa_input.is_visible(timeout=3000):
            self.two_fa_input.fill(secret_2fa or "123456")
            self.verify_2fa_btn.click()
