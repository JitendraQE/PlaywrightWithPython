"""Critical login scenarios."""
import pytest


@pytest.mark.smoke
@pytest.mark.auth
def test_user_can_login_with_valid_credentials(auth_workflow, login_page, valid_user):
    auth_workflow.sign_in(valid_user["username"], valid_user["password"])
    login_page.verify_login_success()


@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.auth
def test_user_cannot_login_with_invalid_credentials(
    auth_workflow, login_page, invalid_user
):
    auth_workflow.sign_in(invalid_user["username"], invalid_user["password"])
    login_page.verify_login_error()


@pytest.mark.validation
@pytest.mark.auth
def test_login_page_displays_required_fields(login_page):
    login_page.open()
    login_page.verify_username_field_visible()
    login_page.login_via_password.click()
    login_page.verify_password_field_visible()
