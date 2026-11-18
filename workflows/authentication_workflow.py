"""Business-level authentication operations."""
import logging

from pages.login_page import LoginPage


logger = logging.getLogger(__name__)


class AuthenticationWorkflow:
    def __init__(self, login_page: LoginPage):
        self.login_page = login_page

    def sign_in(self, username: str, password: str) -> None:
        logger.info("Starting sign-in workflow")
        self.login_page.open()
        self.login_page.login(username, password)

    def sign_out(self) -> None:
        logger.info("Starting sign-out workflow")
        self.login_page.burger_menu.click()
        self.login_page.logout()
