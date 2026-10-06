# White Label CMS — QA Automation

[![QA Pipeline](https://github.com/kostyazkg-svg/white-label-cms-qa/actions/workflows/run-tests.yml/badge.svg)](https://github.com/kostyazkg-svg/white-label-cms-qa/actions/workflows/run-tests.yml)

Фреймворк автотестов на Python + Playwright + Pytest + Allure для white-label шаблона интернет-магазина.

## Что тестируется
**Живой сайт:** https://white-label-cms-kostya61371.amvera.io
**Платформа:** Amvera Cloud
**Тип:** E2E / smoke / responsive
Тесты бьют по реальному прод-URL на Amvera (HTTP + headless Chromium). Никаких моков. Base URL переопределяется через `BASE_URL`.

## Покрытие
- Infrastructure — HTTP 200, Content-Type text/html
- UI Structure — header, footer, h1, непустой title, чистая JS-консоль
- Responsive — нет горизонтального скролла на 375px, viewport 375×812
- Visual — full-page скриншот живого сайта в Allure

## Архитектура
- Page Object Model
- Pydantic Settings через env
- Auto-wait Playwright (без time.sleep)
- Allure: скриншот + URL + HTML при падении
- CI на GitHub Actions с публикацией отчёта на Pages

## Запуск
pip install -r requirements.txt
python -m playwright install chromium
pytest

## Env
BASE_URL = https://white-label-cms-kostya61371.amvera.io
BROWSER = chromium
HEADLESS = true

## Allure-отчёт
https://kostyazkg-svg.github.io/white-label-cms-qa/

## Стек
Python 3.11 · Playwright 1.48 · Pytest 8.3 · Allure 2.13 · Pydantic Settings 2.6 · GitHub Actions

## Автор
Telegram: @reviewpulse_support
Email: kostyazkg@gmail.com