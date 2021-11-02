from lib.support.custom_wait import CustomWait
from lib.support.expected import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from utils.selenium_utils import SeleniumUtils
from lib.elements.button import Button
from lib.elements.static import Static
from lib.elements.text_field import TextField
from utils.logger import Logger
import os
import pytest


class WebAction(CustomWait):

    def __init__(self, driver, model, timeout=30):
        super().__init__(timeout)
        self._driver = driver
        self._model = model
        self.action_chains = ActionChains(self._driver)
        self.log = Logger.get_logger(os.environ.get('PYTEST_CURRENT_TEST').split('::')[-2].split(' ')[0])

    def wait_until_text_display(self, text):
        self.log.info(f"Wait the text [{text}] to display")
        return self.until(TextDisplayOnPage(text), f"cannot see --{text}-- on page")

    def wait_until_element_display(self, element, keyword=None):
        message = f"cannot see --{element}-- on page"
        if keyword:
            message += f" with keyword --{keyword}--"
            self.log.info(f"Wait the element [{element}] identified by [{keyword}] to display")
        else:
            self.log.info(f"Wait the element [{element}] to display")
        return self.until(ElementDisplayOnPage(self._model, element, keyword), message)

    def wait_until_element_disappear(self, element, keyword=None):
        message = f"The element --{element}-- still display on page"
        if keyword:
            message += f" with keyword --{keyword}--"
            self.log.info(f"Wait the element [{element}] identified by [{keyword}] to disappear")
        else:
            self.log.info(f"Wait the element [{element}] to disappear")
        return self.until_not(ElementDisplayOnPage(self._model, element, keyword), message)


    def wait_until_element_match(self, element, keyword):
        message = f"cannot see --{element}-- on page with keyword --{keyword}--"
        self.log.info(f"Wait the element [{element}] which match [{keyword}] to display")
        return self.until(ElementMatchOnPage(self._model, element, keyword), message)

    def click(self, element):
        self.log.info("Perform click on the element")
        body = self._driver.find_element_by_tag_name("body")
        self.action_chains.move_to_element_with_offset(body, element[0], element[1]).click().perform()
        self.action_chains.reset_actions()

    def input(self, element, value):
        self.log.info(f"Input [{value}] to the element")
        body = self._driver.find_element_by_tag_name("body")
        self.action_chains.move_to_element_with_offset(body, element[0], element[1]).click().send_keys(value).perform()
        self.action_chains.reset_actions()

    def browse_page(self, url):
        self.log.info(f"Browser page {url}")
        self._driver.get(url)
        offset, _ = self.check_offset()
        web_test = getattr(pytest, "web_test")
        button = Button(self, offset)
        static = Static(self, offset)
        text_field = TextField(self, offset)
        setattr(web_test, "button", button)
        setattr(web_test, "static", static)
        setattr(web_test, "text_field", text_field)
        setattr(pytest, "web_test", web_test)

    def restart_browser(self, url=None):
        self.log.info(f"Restart browser")
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
