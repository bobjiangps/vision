from lib.support.custom_wait import CustomWait
from lib.support.expected import *
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from utils.selenium_utils import SeleniumUtils
from lib.elements.button import Button
from lib.elements.static import Static
from lib.elements.text_field import TextField
from lib.non_ai_elements.button import NonAiButton
from lib.non_ai_elements.static import NonAiStatic
from lib.non_ai_elements.text_field import NonAiTextField
from lib.non_ai_elements.link import NonAiLink
import pytest


class WebAction(CustomWait):

    def __init__(self, driver, model, logger, timeout=30):
        super().__init__(timeout)
        self._driver = driver
        self._model = model
        self.action_chains = ActionChains(self._driver)
        self.action_builder = ActionBuilder(self._driver)
        self.log = logger

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
        self.action_builder.pointer_action.move_to_location(element[0], element[1])
        self.action_builder.pointer_action.click()
        self.action_builder.perform()

    def input(self, element, value):
        self.log.info(f"Input [{value}] to the element")
        self.action_builder.pointer_action.move_to_location(element[0], element[1])
        self.action_builder.pointer_action.click()
        self.action_builder.perform()
        self.action_chains.send_keys(value).perform()

    def browse_page(self, url):
        self.log.info(f"Browser page {url}")
        self._driver.get(url)
        offset, _ = self.check_offset()
        web_test = getattr(pytest, "web_test")
        setattr(web_test, "button", Button(self, offset))
        setattr(web_test, "static", Static(self, offset))
        setattr(web_test, "text_field", TextField(self, offset))
        setattr(web_test, "non_ai_button", NonAiButton(self))
        setattr(web_test, "non_ai_static", NonAiStatic(self))
        setattr(web_test, "non_ai_text_field", NonAiTextField(self))
        setattr(web_test, "non_ai_link", NonAiLink(self))
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

    def find_non_ai_element_by_coordinates(self, x, y):
        return self._driver.execute_script(f"return document.elementFromPoint({x}, {y});")

    def find_non_ai_element(self, by, value):
        return self._driver.find_element(by, value)

    def find_non_ai_elements(self, by, value):
        return self._driver.find_elements(by, value)

    def wait_until_non_ai_element_present(self, by, value):
        self.log.info("Wait the element present by {0}: '{1}'".format(by, value))
        message = "Unable to check the element present by {0}: '{1}'".format(by, value)
        return self.until(ec.presence_of_element_located((by, value)), message)

    def wait_until_non_ai_element_display(self, by, value):
        self.log.info("Wait the element display by {0}: '{1}'".format(by, value))
        message = "Unable to check the element display by {0}: '{1}'".format(by, value)
        return self.until(ec.visibility_of_element_located((by, value)), message)

    def wait_until_non_ai_element_disappear(self, by, value):
        self.log.info("Wait the element disappear by {0}: '{1}'".format(by, value))
        message = "Unable to check the element disappear by {0}: '{1}'".format(by, value)
        return self.until_not(ec.presence_of_element_located((by, value)), message)

    def wait_until_non_ai_element_clickable(self, by, value):
        self.log.info("Wait the element clickable by {0}: '{1}'".format(by, value))
        message = "Unable to check the element clickable by {0}: '{1}'".format(by, value)
        return self.until(ec.element_to_be_clickable((by, value)), message)

    def wait_until_non_ai_element_selected(self, by, value):
        self.log.info("Wait the element selected by {0}: '{1}'".format(by, value))
        message = "Unable to check the element selected by {0}: '{1}'".format(by, value)
        return self.until(ec.element_located_to_be_selected((by, value)), message)

    def click_non_ai_element(self, element):
        self.log.info("Perform click on the element")
        element.click()

    def input_non_ai_element(self, element, value):
        self.log.info(f"Input [{value}] to the element")
        element.send_keys(value)
