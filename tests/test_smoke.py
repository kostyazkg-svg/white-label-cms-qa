"""Smoke-тесты шаблона White Label CMS."""

from __future__ import annotations

import allure
import pytest
import requests

from config.settings import settings
from pages.main_page import MainPage


@allure.epic("White Label CMS")
@allure.feature("Smoke")
@pytest.mark.smoke
class TestInfrastructure:
    """Доступность и корректность HTTP-слоя."""

    @allure.story("Главная страница отдаёт 200 OK")
    @allure.title("GET / возвращает статус 200")
    def test_main_page_returns_200(self, http_session: requests.Session) -> None:
        with allure.step(f"GET {settings.base_url}"):
            response = http_session.get(str(settings.base_url), timeout=20, allow_redirects=True)
        with allure.step("Проверяем статус-код"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

    @allure.story("Content-Type корректен")
    @allure.title("Главная отдаёт HTML")
    def test_main_page_content_type_is_html(self, http_session: requests.Session) -> None:
        response = http_session.get(str(settings.base_url), timeout=20)
        content_type = response.headers.get("Content-Type", "").lower()
        assert "text/html" in content_type, f"Некорректный Content-Type: {content_type}"


@allure.epic("White Label CMS")
@allure.feature("Smoke")
@pytest.mark.smoke
@pytest.mark.ui
class TestMainPageStructure:
    """Базовая структура главной страницы."""

    @allure.story("Ключевые блоки разметки присутствуют")
    @allure.title("На главной есть header, footer, h1")
    def test_main_page_has_key_blocks(self, page) -> None:
        main_page = MainPage(page).open_main()
        with allure.step("Проверяем шапку"):
            assert main_page.is_header_present(), "Отсутствует <header>"
        with allure.step("Проверяем футер"):
            assert main_page.is_footer_present(), "Отсутствует <footer>"
        with allure.step("Проверяем главный заголовок"):
            assert main_page.is_h1_present(), "Отсутствует <h1>"

    @allure.story("Заголовок вкладки заполнен")
    @allure.title("document.title не пустой")
    def test_page_title_not_empty(self, page) -> None:
        main_page = MainPage(page).open_main()
        title = main_page.title()
        with allure.step(f"Title = '{title}'"):
            assert title.strip(), "Пустой <title>"

    @allure.story("Нет JS-ошибок при загрузке")
    @allure.title("Консоль браузера чистая при первой загрузке")
    def test_no_js_errors_on_load(self, page) -> None:
        errors: list[str] = []

        def on_pageerror(exc):
            errors.append(f"pageerror: {exc}")

        def on_console(msg):
            if msg.type == "error":
                errors.append(f"console.error: {msg.text}")

        page.on("pageerror", on_pageerror)
        page.on("console", on_console)
        MainPage(page).open_main()
        page.wait_for_load_state("networkidle")
        with allure.step(f"Найдено ошибок: {len(errors)}"):
            assert not errors, "JS-ошибки при загрузке:\n" + "\n".join(errors)


@allure.epic("White Label CMS")
@allure.feature("Responsive")
@pytest.mark.mobile
class TestMobileAdaptive:
    """Тесты адаптивности под мобильные устройства."""

    @allure.story("Нет горизонтального скролла")
    @allure.title("На 375px страница помещается по ширине")
    def test_no_horizontal_scroll_on_mobile(self, mobile_page) -> None:
        main_page = MainPage(mobile_page).open_main()
        mobile_page.wait_for_load_state("domcontentloaded")
        with allure.step("Проверяем scrollWidth <= clientWidth"):
            assert main_page.is_mobile_layout(), "Горизонтальный скролл на мобильном"

    @allure.story("Шапка доступна на мобильном")
    @allure.title("Header и навигация рендерятся на 375px")
    def test_header_visible_on_mobile(self, mobile_page) -> None:
        main_page = MainPage(mobile_page).open_main()
        assert main_page.is_header_present(), "Header не виден на мобильном"

    @allure.story("Viewport соответствует мобильному")
    @allure.title("Viewport = 375x812")
    def test_viewport_matches_mobile(self, mobile_page) -> None:
        main_page = MainPage(mobile_page).open_main()
        assert main_page.get_viewport_width() == settings.mobile_viewport_width, (
            f"Viewport {main_page.get_viewport_width()} != {settings.mobile_viewport_width}"
        )
