from lib.support.custom_wait import CustomWait
from lib.support.expected import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from utils.selenium_utils import SeleniumUtils
from lib.elements.button import Button
from lib.elements.static import Static
from lib.elements.text_field import TextField
import pytest


class WebAction(CustomWait):

    def __init__(self, driver, model, timeout=30):
        super().__init__(timeout)
        self._driver = driver
        self._model = model

    def wait_until_text_display(self, text):
        return self.until(TextDisplayOnPage(text), f"cannot see --{text}-- on page")

    def wait_until_element_display(self, element, keyword=None):
        message = f"cannot see --{element}-- on page"
        if keyword:
            message += f" with keyword --{keyword}--"
        return self.until(ElementDisplayOnPage(self._model, element, keyword), message)

    def wait_until_element_match(self, element, keyword):
        message = f"cannot see --{element}-- on page with keyword --{keyword}--"
        return self.until(ElementMatchOnPage(self._model, element, keyword), message)

    def browse_page(self, url):
        self._driver.get(url)
        offset, _ = self.check_offset()
        web_test = getattr(pytest, "web_test")
        button = Button(self._driver, self, offset)
        static = Static(self._driver, self, offset)
        text_field = TextField(self._driver, self, offset)
        setattr(web_test, "button", button)
        setattr(web_test, "static", static)
        setattr(web_test, "text_field", text_field)
        setattr(pytest, "web_test", web_test)

    def restart_browser(self, url=None):
        self._driver = SeleniumUtils.restart_driver()
        web_test = getattr(pytest, "web_test")
        setattr(web_test, "_driver", self._driver)
        setattr(pytest, "web_test", web_test)
        if url:
            self.browse_page(url)

    def check_offset(self):
        v_size = BaseExpectation.get_viewport_size(self._driver)
        b_size = BaseExpectation.get_body_size(self._driver)
        body = self._driver.find_element_by_tag_name("body")
        x = 0
        y = 0
        if v_size[1] != b_size[1]:
            while True:
                try:
                    ActionChains(self._driver).move_to_element_with_offset(body, x, y).click().perform()
                    ActionChains(self._driver).reset_actions()
                    break
                except MoveTargetOutOfBoundsException:
                    y += 10
        return [x, y], body
