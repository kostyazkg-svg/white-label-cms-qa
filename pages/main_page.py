"""Page Object главной страницы."""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница white-label CMS."""

    PATH = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header: Locator = page.locator("header").first
        self.footer: Locator = page.locator("footer").first
        self.navigation: Locator = page.locator("nav").first
        self.h1: Locator = page.locator("h1").first
        self.body: Locator = page.locator("body")
        self.logo: Locator = page.locator("header img, header svg").first
        self.main_content: Locator = page.locator("main, #app, .main, .content").first

    def open_main(self) -> "MainPage":
        self.open(self.PATH)
        return self

    def is_header_present(self) -> bool:
        return self.is_visible(self.header)

    def is_footer_present(self) -> bool:
        return self.is_visible(self.footer)

    def is_navigation_present(self) -> bool:
        return self.is_visible(self.navigation)

    def is_h1_present(self) -> bool:
        return self.is_visible(self.h1)

    def is_logo_present(self) -> bool:
        return self.is_visible(self.logo)

    def get_h1_text(self) -> str:
        if not self.is_visible(self.h1):
            return ""
        return (self.h1.text_content() or "").strip()

    def is_mobile_layout(self) -> bool:
        scroll_width = self.page.evaluate("document.documentElement.scrollWidth")
        client_width = self.page.evaluate("document.documentElement.clientWidth")
        return scroll_width <= client_width + 1

    def get_viewport_width(self) -> int:
        size = self.page.viewport_size
        return int(size["width"]) if size else 0
