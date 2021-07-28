class ElementBase:

    def __init__(self, driver, action, offset):
        self._driver = driver
        self._action = action
        self._offset = offset

    def wait_text_visible(self, **kwargs):
        return self._action.wait_until_text_display(kwargs["text"])

    def wait_element_visible(self, **kwargs):
        return self._action.wait_until_element_display(kwargs["element"], kwargs.get("keyword", None))





