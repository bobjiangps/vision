import pytest
from models.pred import *
from selenium import webdriver
from lib.action.web import WebAction
from lib.elements.button import Button
from lib.elements.static import Static
from lib.elements.text_field import TextField


def pytest_configure():
    print("loading model...")
    setattr(pytest, "model", init_model())


@pytest.fixture(scope="function")
def web():
    web_test = type('web_test', (), {})()
    url = ""
    driver = webdriver.Chrome()
    driver.get(url)
    action = WebAction(driver, getattr(pytest, "model"))
    offset, _ = action.check_offset()
    button = Button(driver, action, offset)
    static = Static(driver, action, offset)
    text_field = TextField(driver, action, offset)
    setattr(web_test, "_driver", driver)
    setattr(web_test, "action", action)
    setattr(web_test, "button", button)
    setattr(web_test, "static", static)
    setattr(web_test, "text_field", text_field)
    yield web_test
    driver.quit()
