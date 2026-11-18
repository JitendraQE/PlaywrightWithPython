# Python + Playwright Enterprise Login Framework

A maintainable starter framework using Python 3.13, Playwright Sync API, Pytest,
Page Object Model, business workflows, YAML configuration and Allure.

## 1. Prerequisites

- Python 3.13
- Git
- Allure command-line tool (optional, for rendering Allure HTML reports)
- Access to a QA/staging application

## 2. Setup

```bash
python3.13 -m venv .venv
source .venv/bin/activate             # macOS/Linux
# .venv\Scripts\activate              # Windows

python -m pip install --upgrade pip
pip install -e .
playwright install chromium
```

For Firefox/WebKit:
```bash
playwright install firefox webkit
```

## 3. Configure the application

1. Update `config/environments/qa.yaml`.
2. Set the real base URL.
3. Confirm login page path, accessible field/button names, success/error text and logout behavior.
4. Copy `.env.example` to `.env`.
5. Set `LOGIN_USERNAME` and `LOGIN_PASSWORD` to a dedicated synthetic QA account.

Never commit `.env` or real credentials.

### Locator contract

The page object uses accessible roles and names configured in each environment's YAML:

- `username_label`
- `password_label`
- `submit_button`

Keep these values aligned with the application's accessibility tree. Prefer stable
`data-testid` selectors if the application exposes them.

## 4. Run tests

```bash
# All tests
pytest

# Smoke tests
pytest -m smoke

# Regression tests
pytest -m regression

# Negative tests
pytest -m negative

# Explicit environment
pytest --env qa

# Firefox (pytest-playwright browser option)
pytest --env qa --browser firefox

# WebKit
pytest --env qa --browser webkit

# Headed mode (edit YAML browser.headless=false)
pytest -m smoke

# Parallel execution
pytest -n 2

# Allure result files
pytest --alluredir=allure-results
allure serve allure-results
```

The `pytest-playwright` plugin provides the `page`, `context`, `browser` and browser
fixtures. Its CLI options can also be used for artifact capture, for example:

```bash
pytest --tracing retain-on-failure \
       --screenshot only-on-failure \
       --video retain-on-failure
```

Timestamped `INFO` logs are printed for every test's start and final outcome,
along with authentication steps and failure screenshot capture. Adjust verbosity
with `pytest --log-cli-level=DEBUG` or `pytest --log-cli-level=WARNING`.
The same logs are saved to `resources/Logs/pytest.log`. Test data and generated HTML/PDF
reports are kept under `resources/` (`resources/test_data/` and
`resources/reporting-labs/`). Credentials are intentionally excluded from framework
log messages.

## 5. Login scenarios included

| Scenario | Test |
|---|---|
| Valid credentials | `test_user_can_login_with_valid_credentials` |
| Invalid credentials | `test_user_cannot_login_with_invalid_credentials` |
| Required fields | `test_login_page_displays_required_fields` |
| Logout | `test_user_can_logout` |
| Login page controls | `test_login_page_opens` |

The expected messages and locators are examples. Align them with the application
under test before execution.

## 6. Architecture rules

- Tests contain business intent and assertions, not raw locator definitions.
- Page objects own selectors and page-level interactions.
- Workflows orchestrate business journeys across pages.
- Configuration is externalized by environment.
- Credentials are injected through environment/CI secret variables.
- Each test should be independent and use isolated browser context state.
- Do not add fixed sleeps. Use Playwright locator actions and web-first assertions.
- Do not use retries to conceal product defects or flaky tests.
- Keep shared base classes small; add abstractions only for repeated behavior.

## 7. CI example (GitLab)

```yaml
stages:
  - test

ui_smoke:
  stage: test
  image: mcr.microsoft.com/playwright/python:v1.50.0-noble
  variables:
    ENV: "qa"
    LOGIN_USERNAME: "$QA_LOGIN_USERNAME"
    LOGIN_PASSWORD: "$QA_LOGIN_PASSWORD"
  script:
    - pip install -e .
    - pytest -m smoke --alluredir=allure-results
  artifacts:
    when: always
    paths:
      - allure-results/
      - artifacts/
    expire_in: 7 days
```

Pin the container image to the Playwright version used by the project. Update both
the image and Python package together after compatibility validation.

## 8. Before production adoption

- Replace example URL, test IDs and expected messages.
- Confirm logout route/behavior.
- Add application-specific password policy and validation cases.
- Add account cleanup and test-data isolation where needed.
- Configure CI secrets and artifact retention.
- Add lint/type-check gates (`ruff check .`, `mypy .`).
- Add ownership, review policy and flaky-test triage process.

## 9. Next extensions

- Registration and password reset workflows
- API-based test data setup/cleanup
- Database verification
- Multi-tenant/application configuration
- Browser matrix and remote execution
- Teams notifications and test analytics
