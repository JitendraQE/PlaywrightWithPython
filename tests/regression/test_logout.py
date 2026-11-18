"""Authenticated session and logout scenarios."""
import pytest
from playwright.sync_api import expect
from reporting_labs import meta, step, test_data


@pytest.mark.regression
@pytest.mark.auth
@pytest.mark.meta(priority="P1", owner="JK", feature="login", story="Login-2")
def test_user_can_logout(auth_workflow, login_page, valid_user):
    with step("Log in Authenticated user"):
        auth_workflow.sign_in(valid_user["username"], valid_user["password"])
    with step("After successful login, user can log out"):
        login_page.verify_login_success()
        auth_workflow.sign_out()
        expect(login_page.username_input).to_be_visible()
