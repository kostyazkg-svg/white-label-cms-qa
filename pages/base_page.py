"""Базовый класс страницы."""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from config.settings import settings


class BasePage:
    """Базовый Page Object."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(settings.default_timeout_ms)
        self.page.set_default_navigation_timeout(settings.navigation_timeout_ms)

    def open(self, path: str = "/") -> "BasePage":
        """Открыть относительный путь."""
        url = str(settings.base_url).rstrip("/") + path
        self.page.goto(url, wait_until="domcontentloaded")
        return self

    def current_url(self) -> str:
        return self.page.url

    def title(self) -> str:
        return self.page.title()

    def wait_visible(self, locator: Locator, timeout: int | None = None) -> Locator:
        expect(locator).to_be_visible(timeout=timeout or settings.default_timeout_ms)
        return locator

    def wait_hidden(self, locator: Locator, timeout: int | None = None) -> None:
        expect(locator).to_be_hidden(timeout=timeout or settings.default_timeout_ms)

    def safe_click(self, locator: Locator) -> None:
        expect(locator).to_be_enabled()
        expect(locator).to_be_visible()
        locator.click()

    def safe_fill(self, locator: Locator, value: str) -> None:
        expect(locator).to_be_visible()
        locator.fill("")
        locator.fill(value)
        expect(locator).to_have_value(value)

    def safe_text(self, locator: Locator) -> str:
        self.wait_visible(locator)
        return (locator.text_content() or "").strip()

    def is_visible(self, locator: Locator, timeout: int = 3_000) -> bool:
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def count(self, locator: Locator) -> int:
        return locator.count()

    def expect_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    def expect_text_contains(self, locator: Locator, fragment: str) -> None:
        expect(locator).to_contain_text(fragment)
