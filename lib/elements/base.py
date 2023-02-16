from conf.default import *


class ElementBase:

    _action = None

    def __init__(self, offset=None, text=None, element_type=None, keyword=None, direction=None, beyond=True, refer=None):
        self._offset = [0, 0] if not offset else offset
        self.text = text
        self.element_type = element_type
        self.keyword = keyword
        self.direction = direction
        self.beyond = beyond
        self.refer = refer

    @classmethod
    def set_action(cls, value):
        cls._action = value

    def _produce(self):
        # self.__class__(self._action, self._offset, self.text, self.element_type, self.keyword)
        # or
        return type(self)(self._offset, self.text, self.element_type, self.keyword)

    def element(self, timeout=None):
        if self.refer:
            return self._action.wait_until_element_by_region_display(self, timeout)
        else:
            return self._action.wait_until_display(self, timeout)

    def elements(self, timeout=None):
        return self._action.wait_until_elements_display(self, timeout)

    def wait_element_visible(self, timeout=None):
        if self.refer:
            return self._action.wait_until_element_by_region_display(self, timeout)
        else:
            return self._action.wait_until_display(self, timeout)

    def wait_element_invisible(self, timeout=None):
        if self.refer:
            return self._action.wait_until_element_by_region_disappear(self, timeout)
        else:
            return self._action.wait_until_disappear(self, timeout)

    def action_click(self, element):
        self._action.click((element[0] + self._offset[0], element[1] + self._offset[1]))

    def action_input(self, element, value):
        if value:
            self._action.input((element[0] + self._offset[0], element[1] + self._offset[1]), value)

    def action_clear(self, element):
        self._action.clear((element[0] + self._offset[0], element[1] + self._offset[1]))

    def action_press_key(self, element, key):
        self._action.press_key((element[0] + self._offset[0], element[1] + self._offset[1]), key)

    def action_send_value(self, element, value):
        self._action.send_value((element[0] + self._offset[0], element[1] + self._offset[1]), value)

    def move_to(self, *args):
        element = self.wait_element_visible()
        self.action.move_to_element(element)

    def is_visible(self):
        return self._action.is_displayed(self)
