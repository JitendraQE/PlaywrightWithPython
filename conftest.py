"""Shared Pytest fixtures and failure evidence."""
import logging
import os
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from config.settings import load_config
from pages.login_page import LoginPage
from workflows.authentication_workflow import AuthenticationWorkflow


logger = logging.getLogger("framework.tests")

load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Environment config name")


def pytest_configure(config):
    env_name = config.getoption("--env") or os.getenv("ENV", "qa")
    os.environ["ENV"] = env_name


@pytest.fixture(scope="session")
def framework_config(pytestconfig):
    return load_config(pytestconfig.getoption("--env"))


@pytest.fixture(scope="session")
def browser_type_launch_args(framework_config):
    return {
        "headless": framework_config.browser.headless,
        "slow_mo": framework_config.browser.slow_mo_ms,
    }


@pytest.fixture(scope="session")
def browser_context_args(framework_config):
    return {
        "viewport": {
            "width": framework_config.browser.viewport.width,
            "height": framework_config.browser.viewport.height,
        },
        "ignore_https_errors": False,
    }


@pytest.fixture(autouse=True)
def set_expect_timeout(framework_config):
    from playwright.sync_api import expect
    expect.set_options(timeout=framework_config.timeouts.expect_ms)


@pytest.fixture
def login_page(page: Page, framework_config):
    page.set_default_navigation_timeout(framework_config.timeouts.navigation_ms)
    return LoginPage(
        page=page,
        base_url=framework_config.application.base_url,
        login_config=framework_config.login,
        action_timeout_ms=framework_config.timeouts.action_ms,
    )


@pytest.fixture
def auth_workflow(login_page):
    return AuthenticationWorkflow(login_page)


@pytest.fixture
def valid_user():
    username = os.getenv("LOGIN_USERNAME")
    password = os.getenv("LOGIN_PASSWORD")
    if not username or not password:
        pytest.skip("Set LOGIN_USERNAME and LOGIN_PASSWORD to run valid-login tests.")
    return {"username": username, "password": password}


@pytest.fixture
def invalid_user():
    return {
        "username": "invalid.user@example.test",
        "password": "incorrect-password",
    }


def pytest_runtest_logstart(nodeid, location):
    logger.info("START %s (%s:%s)", nodeid, location[0], location[1])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "teardown":
        reports = [
            getattr(item, f"rep_{phase}", None)
            for phase in ("setup", "call", "teardown")
        ]

        failed_report = next(
            (phase_report for phase_report in reports if phase_report and phase_report.failed),
            None,
        )

        skipped_report = next(
            (phase_report for phase_report in reports if phase_report and phase_report.skipped),
            None,
        )

        if failed_report:
            logger.error("FAIL %s (phase: %s)", item.nodeid, failed_report.when)
        elif skipped_report:
            logger.warning("SKIP %s", item.nodeid)
        else:
            logger.info("PASS %s", item.nodeid)

    if report.when != "call" or not report.failed or call.excinfo is None:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    artifacts_dir = Path("artifacts") / "failures"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    safe_name = item.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")

    try:
        screenshot_path = artifacts_dir / f"{safe_name}.png"

        page.screenshot(path=str(screenshot_path), full_page=True)

        logger.info("Failure screenshot saved: %s", screenshot_path)

    except Exception as exc:
        logger.warning(
            "Could not capture failure screenshot for %s: %s",
            item.nodeid,
            exc,
        )
        item.warn(
            pytest.PytestWarning(f"Could not capture failure screenshot: {exc}")
        )