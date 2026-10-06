"""Общие фикстуры Pytest."""

from __future__ import annotations

from typing import Generator

import allure
import pytest
import requests
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config.settings import settings


@pytest.fixture(scope="session")
def http_session() -> Generator[requests.Session, None, None]:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "WhiteLabelCMS-QA/1.0 (+github actions)",
        "Accept": "text/html,application/xhtml+xml",
    })
    yield session
    session.close()


@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    with sync_playwright() as pw:
        browser_type = getattr(pw, settings.browser)
        browser = browser_type.launch(headless=settings.headless)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def desktop_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(
        viewport={"width": settings.desktop_viewport_width, "height": settings.desktop_viewport_height},
        locale="ru-RU",
        timezone_id="Europe/Moscow",
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def mobile_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(
        viewport={"width": settings.mobile_viewport_width, "height": settings.mobile_viewport_height},
        device_scale_factor=3,
        is_mobile=True,
        has_touch=True,
        locale="ru-RU",
        timezone_id="Europe/Moscow",
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(desktop_context: BrowserContext) -> Generator[Page, None, None]:
    page = desktop_context.new_page()
    yield page
    _finalize_page(page)


@pytest.fixture(scope="function")
def mobile_page(mobile_context: BrowserContext) -> Generator[Page, None, None]:
    page = mobile_context.new_page()
    yield page
    _finalize_page(page)


def _finalize_page(page: Page) -> None:
    try:
        page.close()
    except Exception:
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    page = item.funcargs.get("page") or item.funcargs.get("mobile_page")
    if page is None:
        return

    try:
        allure.attach(page.url, name="URL at failure", attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass

    try:
        screenshot = page.screenshot(full_page=True, type="png")
        allure.attach(screenshot, name="screenshot-on-failure", attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass

    try:
        html = page.content()
        allure.attach(html[:100_000], name="page-source-on-failure", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass
