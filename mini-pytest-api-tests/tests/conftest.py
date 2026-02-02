import logging

import pytest

from apitest.client import ApiClient
from apitest.config import settings


@pytest.fixture(scope="session")
def api_client():
    """Shared API client session."""
    client = ApiClient()
    yield client
    client.session.close()


# Hook for adding info to the HTML report
def pytest_html_report_title(report):
    report.title = "Mini API Test Report"


def pytest_configure(config):
    config.stash["env"] = settings.base_url


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Add extra info to report if needed


@pytest.fixture(scope="session", autouse=True)
def log_test_run_start():
    logging.info(f"Starting test run on Environment: {settings.base_url}")
