from playwright.sync_api import Page, expect

class BasePage:
    """Base Page Object class encapsulating common Playwright web-first actions."""
    
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def wait_for_url_match(self, pattern: str, timeout: int = 15000):
        expect(self.page).to_have_url(pattern, timeout=timeout)

    def get_title(self) -> str:
        return self.page.title()
