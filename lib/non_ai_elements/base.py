from selenium.webdriver.support import expected_conditions as ec
from utils.logger import Logger
import os


class NonAiElementBase:

    def __init__(self, action):
        self._action = action
        self.identify_type = None
        self.identify_value = None
        self.log = Logger.get_logger(os.environ.get('PYTEST_CURRENT_TEST').split('::')[-2].split(' ')[0])

    def element(self):
        return self._action._driver.find_element(self.identify_type, self.identify_value)

    def elements(self):
        return self._action._driver.find_elements(self.identify_type, self.identify_value)

    def wait_element_present(self):
        self.log.info("Wait the element present by {0}: '{1}'".format(self.identify_type, self.identify_value))
        message = "Unable to check the element present by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until(ec.presence_of_element_located((self.identify_type, self.identify_value)), message)

    def wait_element_visible(self):
        self.log.info("Wait the element visible by {0}: '{1}'".format(self.identify_type, self.identify_value))
        message = "Unable to check the element visible by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until(ec.visibility_of_element_located((self.identify_type, self.identify_value)), message)

    def wait_element_disappear(self):
        self.log.info("Wait the element disappear by {0}: '{1}'".format(self.identify_type, self.identify_value))
        message = "Unable to wait the element disappear by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until_not(ec.presence_of_element_located((self.identify_type, self.identify_value)), message)

    def wait_element_clickable(self):
        self.log.info("Wait the element clickable by {0}: '{1}'".format(self.identify_type, self.identify_value))
        message = "Unable to check the element clickable by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until(ec.element_to_be_clickable((self.identify_type, self.identify_value)), message)

    def wait_element_selected(self):
        self.log.info("Wait the element selected by {0}: '{1}'".format(self.identify_type, self.identify_value))
        message = "Unable to check the element selected by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until(ec.element_located_to_be_selected((self.identify_type, self.identify_value)), message)

    def action_click(self, element):
        self.log.info("Perform click on the element")
        element.click()

    def action_input(self, element, value):
        self.log.info(f"Input [{value}] to the element")
        element.send_keys(value)
