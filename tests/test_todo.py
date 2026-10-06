"""E2E-тесты приложения To-Do List (Selenium + pytest)."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

INPUT = (By.ID, "todo-input")
ADD_BTN = (By.ID, "add-btn")
ITEMS = (By.CSS_SELECTOR, "#todo-list .todo-item")
ERROR = (By.ID, "error")
COUNTER = (By.ID, "counter")


def add_task(driver, text):
    """Вводит текст и нажимает кнопку «Добавить»."""
    driver.find_element(*INPUT).send_keys(text)
    driver.find_element(*ADD_BTN).click()


def wait_items_count(driver, expected):
    """Явное ожидание: в списке ровно expected задач."""
    WebDriverWait(driver, 5).until(
        lambda d: len(d.find_elements(*ITEMS)) == expected
    )


def test_page_title_and_empty_list(driver):
    assert driver.title == "To-Do List"
    assert driver.find_elements(*ITEMS) == []
    assert driver.find_element(*COUNTER).text == "Осталось задач: 0"


def test_add_task(driver):
    add_task(driver, "Купить молоко")
    wait_items_count(driver, 1)

    item = driver.find_element(*ITEMS)
    assert "Купить молоко" in item.text
    assert driver.find_element(*COUNTER).text == "Осталось задач: 1"
    # после добавления поле ввода очищается
    assert driver.find_element(*INPUT).get_attribute("value") == ""


def test_add_task_by_enter_key(driver):
    driver.find_element(*INPUT).send_keys("Позвонить маме", Keys.ENTER)
    wait_items_count(driver, 1)


def test_empty_task_is_not_added(driver):
    driver.find_element(*ADD_BTN).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located(ERROR))
    assert driver.find_elements(*ITEMS) == []


def test_complete_task(driver):
    add_task(driver, "Сделать ПР №7")
    wait_items_count(driver, 1)

    driver.find_element(By.CSS_SELECTOR, ".todo-text").click()
    item = driver.find_element(*ITEMS)
    assert "done" in item.get_attribute("class")
    assert driver.find_element(*COUNTER).text == "Осталось задач: 0"


def test_delete_task(driver):
    add_task(driver, "Удаляемая задача")
    wait_items_count(driver, 1)

    driver.find_element(By.CSS_SELECTOR, ".delete-btn").click()
    wait_items_count(driver, 0)
    assert driver.find_element(*COUNTER).text == "Осталось задач: 0"


@pytest.mark.parametrize("tasks", [
    ["Первая", "Вторая"],
    ["Задача 1", "Задача 2", "Задача 3"],
])
def test_add_several_tasks(driver, tasks):
    for text in tasks:
        add_task(driver, text)
    wait_items_count(driver, len(tasks))
    assert driver.find_element(*COUNTER).text == f"Осталось задач: {len(tasks)}"
