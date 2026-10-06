"""Общие фикстуры для E2E-тестов."""
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Путь к index.html вычисляется относительно репозитория,
# поэтому тесты работают и локально, и в GitHub Actions
APP_URL = (Path(__file__).resolve().parent.parent / "index.html").as_uri()


@pytest.fixture
def driver():
    """Запускает Chrome в headless-режиме и закрывает его после теста."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")             # нужно на CI-серверах
    options.add_argument("--disable-dev-shm-usage")  # на CI мало /dev/shm
    options.add_argument("--window-size=1280,900")

    drv = webdriver.Chrome(options=options)  # Selenium Manager сам найдёт драйвер
    drv.get(APP_URL)
    yield drv
    drv.quit()
