from conf.default import *


class ElementBase:

    _action = None

    def __init__(self, offset=None, text=None, element_type=None, keyword=None, direction=None):
        self._offset = [0, 0] if not offset else offset
        self.text = text
        self.element_type = element_type
        self.keyword = keyword
        self.direction = direction

    @classmethod
    def set_action(cls, value):
        cls._action = value

    def _produce(self):
        # self.__class__(self._action, self._offset, self.text, self.element_type, self.keyword)
        # or
        return type(self)(self._offset, self.text, self.element_type, self.keyword)

    def wait_text_visible(self, timeout=default_timeout):
        return self._action.wait_until_text_display(self.text, timeout)

    def wait_element_visible(self, timeout=default_timeout):
        return self._action.wait_until_element_display(self.element_type, self.keyword, timeout)

    def wait_element_disappear(self, timeout=default_timeout):
        return self._action.wait_until_element_disappear(self.element_type, self.keyword, timeout)

    def wait_element_match_visible(self, timeout=default_timeout):
        return self._action.wait_until_element_match(self.element_type, self.keyword, self.direction, timeout)

    def wait_element_match_disappear(self, timeout=default_timeout):
        return self._action.wait_until_element_match_disappear(self.element_type, self.keyword, self.direction, timeout)

    def action_click(self, element):
        self._action.click((element[0], element[1] + self._offset[1]))

    def action_input(self, element, value):
        self._action.input((element[0], element[1] + self._offset[1]), value)
