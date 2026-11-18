"""Common page behavior. Keep this class small and application-agnostic."""
from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page, base_url: str, action_timeout_ms: int = 10_000):
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.page.set_default_timeout(action_timeout_ms)

    def navigate_to(self, path: str) -> None:
        self.page.goto(f"{self.base_url}/{path.lstrip('/')}", wait_until="domcontentloaded")

    def click(self, locator: Locator) -> None:
        locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        locator.fill(value)

    def current_url(self) -> str:
        return self.page.url
