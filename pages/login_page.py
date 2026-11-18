"""Page object for the login screen."""
import logging

from playwright.sync_api import Locator, Page, expect

from core.base_page import BasePage
from config.settings import LoginConfig


logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    def __init__(
        self,
        page: Page,
        base_url: str,
        login_config: LoginConfig,
        action_timeout_ms: int = 10_000,
    ):
        super().__init__(page, base_url, action_timeout_ms)
        self.config = login_config
        self.username_input: Locator = page.get_by_role(
            "textbox", name=login_config.username_label, exact=True
        )
        self.password_input: Locator = page.get_by_role(
            "textbox", name=login_config.password_label, exact=True
        )
        self.submit_button: Locator = page.get_by_role(
            "button", name=login_config.submit_button, exact=True
        )
        self.login_via_password: Locator = page.get_by_text("Login via Password", exact=True)
        self.error_message: Locator = page.get_by_text(login_config.error_indicator, exact=False)
        self.burger_menu: Locator = page.locator('div.profile_dropdown > svg > path')
        self.logout_button: Locator = page.get_by_role(
            "link", name=login_config.logout_button, exact=True
        )

    def open(self) -> None:
        logger.info("Opening login page")
        self.navigate_to(self.config.path)

    def enter_username(self, username: str) -> None:
        self.username_input.fill(username)

    def enter_password(self, password: str) -> None:
        self.password_input.fill(password)

    def submit(self) -> None:
        logger.info("Submitting login form")
        self.submit_button.click()

    def login(self, username: str, password: str) -> None:
        self.login_via_password.click()
        self.enter_username(username)
        self.enter_password(password)
        self.submit()

    def verify_login_success(self) -> None:
        expect(self.burger_menu).to_be_visible()

    def verify_login_error(self) -> None:
        expect(self.error_message).to_be_visible()

    def verify_username_field_visible(self) -> None:
        expect(self.username_input).to_be_visible()

    def verify_password_field_visible(self) -> None:
        expect(self.password_input).to_be_visible()

    def logout(self) -> None:
        logger.info("Selecting logout")
        self.logout_button.click()
