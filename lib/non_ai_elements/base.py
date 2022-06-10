from conf.default import *


class NonAiElementBase:

    _action = None

    def __init__(self, identify_type=None, identify_value=None):
        self.identify_type = identify_type
        self.identify_value = identify_value

    @classmethod
    def set_action(cls, value):
        cls._action = value

    def _produce(self):
        # self.__class__(self._action, self.identify_type, self.identify_value)
        # or
        return type(self)(self.identify_type, self.identify_value)

    def element(self):
        return self._action.find_non_ai_element(self.identify_type, self.identify_value)

    def elements(self):
        return self._action.find_non_ai_elements(self.identify_type, self.identify_value)

    def wait_element_present(self, timeout=None):
        return self._action.wait_until_non_ai_element_present(self.identify_type, self.identify_value, timeout)

    def wait_element_visible(self, timeout=None):
        return self._action.wait_until_non_ai_element_display(self.identify_type, self.identify_value, timeout)

    def wait_element_disappear(self, timeout=None):
        return self._action.wait_until_non_ai_element_disappear(self.identify_type, self.identify_value, timeout)

    def wait_element_clickable(self, timeout=None):
        return self._action.wait_until_non_ai_element_clickable(self.identify_type, self.identify_value, timeout)

    def wait_element_selected(self, timeout=None):
        return self._action.wait_until_non_ai_element_selected(self.identify_type, self.identify_value, timeout)

    def action_click(self, element):
        self._action.click_non_ai_element(element)

    def action_input(self, element, value):
        self._action.input_non_ai_element(element, value)
