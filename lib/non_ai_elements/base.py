from conf.default import *


class NonAiElementBase:

    def __init__(self, action, identify_type=None, identify_value=None):
        self._action = action
        self.identify_type = identify_type
        self.identify_value = identify_value

    def _produce(self):
        # self.__class__(self._action, self.identify_type, self.identify_value)
        # or
        return type(self)(self._action, self.identify_type, self.identify_value)

    def element(self):
        return self._action.find_non_ai_element(self.identify_type, self.identify_value)

    def elements(self):
        return self._action.find_non_ai_elements(self.identify_type, self.identify_value)

    def wait_element_present(self, timeout=default_timeout):
        return self._action.wait_until_non_ai_element_present(self.identify_type, self.identify_value, timeout)

    def wait_element_visible(self, timeout=default_timeout):
        return self._action.wait_until_non_ai_element_display(self.identify_type, self.identify_value, timeout)

    def wait_element_disappear(self, timeout=default_timeout):
        return self._action.wait_until_non_ai_element_disappear(self.identify_type, self.identify_value, timeout)

    def wait_element_clickable(self, timeout=default_timeout):
        return self._action.wait_until_non_ai_element_clickable(self.identify_type, self.identify_value, timeout)

    def wait_element_selected(self, timeout=default_timeout):
        return self._action.wait_until_non_ai_element_selected(self.identify_type, self.identify_value, timeout)

    def action_click(self, element):
        self._action.click_non_ai_element(element)

    def action_input(self, element, value):
        self._action.input_non_ai_element(element, value)
