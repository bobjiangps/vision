class ElementBase:

    def __init__(self, action, offset):
        self._action = action
        self._offset = offset

    def wait_text_visible(self, **kwargs):
        return self._action.wait_until_text_display(kwargs["text"])

    def wait_element_visible(self, **kwargs):
        return self._action.wait_until_element_display(kwargs["element"], kwargs.get("keyword", None))

    def wait_element_match_visible(self, **kwargs):
        return self._action.wait_until_element_match(kwargs["element"], kwargs["keyword"])

    def action_click(self, element):
        self._action.click((element[0], element[1] + self._offset[1]))

    def action_input(self, element, value):
        self._action.input((element[0], element[1] + self._offset[1]), value)
