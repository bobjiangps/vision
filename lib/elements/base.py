class ElementBase:

    def __init__(self, action, offset, text=None, element_type=None, keyword=None):
        self._action = action
        self._offset = offset
        self.text = text
        self.element_type = element_type
        self.keyword = keyword

    def wait_text_visible(self):
        return self._action.wait_until_text_display(self.text)

    def wait_element_visible(self):
        return self._action.wait_until_element_display(self.element_type, self.keyword)

    def wait_element_disappear(self):
        return self._action.wait_until_element_disappear(self.element_type, self.keyword)

    def wait_element_match_visible(self):
        return self._action.wait_until_element_match(self.element_type, self.keyword)

    def action_click(self, element):
        self._action.click((element[0], element[1] + self._offset[1]))

    def action_input(self, element, value):
        self._action.input((element[0], element[1] + self._offset[1]), value)

    def _produce(self):
        # self.__class__(self._action, self._offset, self.text, self.element_type, self.keyword)
        # or
        return type(self)(self._action, self._offset, self.text, self.element_type, self.keyword)
