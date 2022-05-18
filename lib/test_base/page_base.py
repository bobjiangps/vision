from lib.elements import *
from lib.non_ai_elements import *
from lib.action.web import WebAction
from utils.selenium_utils import SeleniumUtils
import pytest


class PageBase:

    log = None
    _driver = None
    action = None

    @classmethod
    def restart_browser(cls):
        cls._driver = SeleniumUtils.restart_driver()
        cls.action = WebAction(cls._driver, getattr(pytest, "model"), cls.log)
        ElementBase.set_action(cls.action)
        NonAiElementBase.set_action(cls.action)

    @classmethod
    def browse_page(cls, url):
        cls.log.info(f"Browser page {url}")
        cls._driver.maximize_window()
        cls._driver.get(url)
