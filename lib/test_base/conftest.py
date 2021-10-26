import pytest
from models.pred import *
from utils.selenium_utils import SeleniumUtils
from lib.action.web import WebAction


def pytest_configure():
    print("loading model...")
    setattr(pytest, "model", init_model())


@pytest.fixture(scope="function")
def web():
    web_test = type('web_test', (), {})()
    url = ""
    driver = SeleniumUtils.get_driver("Chrome")
    action = WebAction(driver, getattr(pytest, "model"))
    setattr(web_test, "_driver", driver)
    setattr(web_test, "action", action)
    setattr(pytest, "web_test", web_test)
    action.browse_page(url)
    yield web_test
    SeleniumUtils.quit_driver()
