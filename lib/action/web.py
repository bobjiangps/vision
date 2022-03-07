from lib.support.custom_wait import CustomWait
from lib.support.expected import *
from conf.default import *
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from utils.selenium_utils import SeleniumUtils
from lib.elements import *
from lib.non_ai_elements import *
import pytest


class WebAction(CustomWait):

    def __init__(self, driver, model, logger, timeout=default_timeout):
        super().__init__(driver, timeout)
        self._driver = driver
        self._model = model
        self.action_chains = ActionChains(self._driver)
        self.action_builder = ActionBuilder(self._driver)
        self.log = logger
        self.timeout = timeout

    def wait_until_text_display(self, text, timeout=default_timeout):
        self.log.info(f"Wait the text [{text}] to display")
        return self.until(TextDisplayOnPage(text), f"cannot see --{text}-- on page after wait {timeout} seconds") \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until(TextDisplayOnPage(text), f"cannot see --{text}-- on page")

    def wait_until_element_display(self, element, keyword=None, timeout=default_timeout):
        message = f"cannot see --{element}-- on page after wait {timeout} seconds"
        if keyword:
            message += f" with keyword --{keyword}--"
            self.log.info(f"Wait the element [{element}] identified by [{keyword}] to display")
        else:
            self.log.info(f"Wait the element [{element}] to display")
        return self.until(ElementDisplayOnPage(self._model, element, keyword), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until(ElementDisplayOnPage(self._model, element, keyword), message)

    def wait_until_element_disappear(self, element, keyword=None, timeout=default_timeout):
        message = f"The element --{element}-- still display on page after wait {timeout} seconds"
        if keyword:
            message += f" with keyword --{keyword}--"
            self.log.info(f"Wait the element [{element}] identified by [{keyword}] to disappear")
        else:
            self.log.info(f"Wait the element [{element}] to disappear")
        return self.until_not(ElementDisplayOnPage(self._model, element, keyword), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until_not(ElementDisplayOnPage(self._model, element, keyword), message)

    def wait_until_element_match(self, element, keyword, direction, timeout=default_timeout):
        message = f"cannot see --{element}-- on page with keyword --{keyword}-- after wait {timeout} seconds"
        self.log.info(f"Wait the element [{element}] which match [{keyword}] to display")
        return self.until(ElementMatchOnPage(self._model, element, keyword, direction), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until(ElementMatchOnPage(self._model, element, keyword, direction), message)

    def wait_until_element_match_disappear(self, element, keyword, direction, timeout=default_timeout):
        message = f"The element --{element}-- still display on page with keyword --{keyword}-- after wait {timeout} seconds"
        self.log.info(f"Wait the element [{element}] which match [{keyword}] to disappear")
        return self.until_not(ElementMatchOnPage(self._model, element, keyword, direction), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until_not(ElementMatchOnPage(self._model, element, keyword, direction), message)

    def click(self, element):
        self.log.info("Perform click on the element")
        self.action_builder.pointer_action.move_to_location(element[0], element[1])
        self.action_builder.pointer_action.click()
        self.action_builder.perform()
        self.clear_actions(self.action_builder)

    def input(self, element, value):
        self.log.info(f"Input [{value}] to the element")
        self.action_builder.pointer_action.move_to_location(element[0], element[1])
        self.action_builder.pointer_action.click()
        self.action_builder.perform()
        self.clear_actions(self.action_builder)
        self.action_chains.send_keys(value).perform()
        self.clear_actions(self.action_chains)

    def scroll_to_bottom(self):
        self._driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")

    def scroll_to_top(self):
        self._driver.execute_script("window.scrollTo(0, 0);")

    def scroll_by(self, x=0, y=500):
        self._driver.execute_script(f"window.scrollBy({x}, {y});")

    @staticmethod
    # for selenium 3, cannot reset actions
    def clear_actions(item):
        if hasattr(item, "w3c_actions"):
            for device in item.w3c_actions.devices:
                device.clear_actions()
        else:
            for device in item.devices:
                device.clear_actions()

    def browse_page(self, url):
        self.log.info(f"Browser page {url}")
        self._driver.get(url)

    def restart_browser(self):
        self.log.info(f"Restart browser")
        return SeleniumUtils.restart_driver()

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

    def find_non_ai_element_by_coordinates(self, x, y):
        return self._driver.execute_script(f"return document.elementFromPoint({x}, {y});")

    def find_non_ai_element(self, by, value):
        return self._driver.find_element(by, value)

    def find_non_ai_elements(self, by, value):
        return self._driver.find_elements(by, value)

    def wait_until_non_ai_element_present(self, by, value, timeout=default_timeout):
        self.log.info(f"Wait the element present by {by}: {value}")
        message = f"Unable to check the element present by {by}: {value} after wait {timeout} seconds"
        return self.until(ec.presence_of_element_located((by, value)), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until(ec.presence_of_element_located((by, value)), message)

    def wait_until_non_ai_element_display(self, by, value, timeout=default_timeout):
        self.log.info(f"Wait the element display by {by}: {value}")
        message = f"Unable to check the element display by {by}: {value} after wait {timeout} seconds"
        return self.until(ec.visibility_of_element_located((by, value)), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until(ec.visibility_of_element_located((by, value)), message)

    def wait_until_non_ai_element_disappear(self, by, value, timeout=default_timeout):
        self.log.info(f"Wait the element disappear by {by}: {value}")
        message = f"Unable to check the element disappear by {by}: {value} after wait {timeout} seconds"
        return self.until_not(ec.presence_of_element_located((by, value)), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until_not(ec.presence_of_element_located((by, value)), message)

    def wait_until_non_ai_element_clickable(self, by, value, timeout=default_timeout):
        self.log.info(f"Wait the element clickable by {by}: {value}")
        message = f"Unable to check the element clickable by {by}: {value} after wait {timeout} seconds"
        return self.until(ec.element_to_be_clickable((by, value)), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until(ec.element_to_be_clickable((by, value)), message)

    def wait_until_non_ai_element_selected(self, by, value, timeout=default_timeout):
        self.log.info(f"Wait the element selected by {by}: {value}")
        message = f"Unable to check the element selected by {by}: {value} after wait {timeout} seconds"
        return self.until(ec.element_located_to_be_selected((by, value)), message) \
            if timeout == self.timeout else \
            CustomWait(self._driver, timeout).until(ec.element_located_to_be_selected((by, value)), message)

    def click_non_ai_element(self, element):
        self.log.info("Perform click on the element")
        element.click()

    def input_non_ai_element(self, element, value):
        self.log.info(f"Input [{value}] to the element")
        element.send_keys(value)
