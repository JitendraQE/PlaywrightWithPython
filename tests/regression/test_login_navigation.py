"""Login route and basic UI availability checks."""
import pytest
from playwright.sync_api import expect
from reporting_labs import meta, step, test_data
@pytest.mark.regression
@pytest.mark.meta(priority="P1", owner="JK", feature="login", story="Login-1")
def test_login_page_opens(login_page):
    login_page.open()
    with step("Log in"):
        login_page.login_via_password.click()
        expect(login_page.username_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()
        expect(login_page.submit_button).to_be_visible()