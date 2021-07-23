from common.support.custom_wait import CustomWait
from common.support.expected import *


class WebAction(CustomWait):

    def __init__(self, driver, model, timeout=30):
        super().__init__(timeout)
        self._driver = driver
        self._model = model

    def wait_until_text_display(self, text):
        self.until(TextDisplayOnPage(text), f"cannot see --{text}-- on page")

    def wait_until_element_display(self, element, keyword):
        pass
