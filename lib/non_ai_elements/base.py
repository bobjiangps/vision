from selenium.webdriver.support import expected_conditions as ec


class NonAiElementBase:

    def __init__(self, action):
        self._action = action
        self.identify_type = None
        self.identify_value = None

    def element(self):
        return self._action._driver.find_element(self.identify_type, self.identify_value)

    def elements(self):
        return self._action._driver.find_elements(self.identify_type, self.identify_value)

    def wait_element_present(self):
        message = "Unable to check the element present by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until(ec.presence_of_element_located((self.identify_type, self.identify_value)), message)

    def wait_element_visible(self):
        message = "Unable to check the element visible by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until(ec.visibility_of_element_located((self.identify_type, self.identify_value)), message)

    def wait_element_disappear(self):
        message = "Unable to wait the element disappear by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until_not(ec.presence_of_element_located((self.identify_type, self.identify_value)), message)

    def wait_element_clickable(self):
        message = "Unable to check the element clickable by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until(ec.element_to_be_clickable((self.identify_type, self.identify_value)), message)

    def wait_element_selected(self):
        message = "Unable to check the element selected by {0}: '{1}'".format(self.identify_type, self.identify_value)
        return self._action.until(ec.element_located_to_be_selected((self.identify_type, self.identify_value)), message)
