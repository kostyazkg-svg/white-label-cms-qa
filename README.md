# White Label CMS — QA Automation

[![QA Pipeline](https://github.com/ТВОЙ_ЛОГИН/white-label-cms-qa/actions/workflows/run-tests.yml/badge.svg)](https://github.com/ТВОЙ_ЛОГИН/white-label-cms-qa/actions/workflows/run-tests.yml)

Пет-проект для портфолио: фреймворк автотестов на Python + Playwright + Pytest + Allure
для white-label шаблона интернет-магазина на Amvera.

## Что тестируется
- Smoke: доступность (200 OK), Content-Type, консоль браузера
- UI: header, footer, h1, непустой title
- Mobile: отсутствие горизонтального скролла на 375px

## Архитектура
- Page Object Model
- Pydantic Settings
- Auto-wait Playwright (без time.sleep)
- Allure: скриншот full-page + URL + HTML при падении

## Запуск
pip install -r requirements.txt
python -m playwright install chromium
pytest

## Автор
Telegram: @reviewpulse_support
Email: kostyazkg@gmail.com
