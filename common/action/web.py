from common.support.custom_wait import CustomWait
from common.support.expected import *
from conf.config import LoadConfig
from pathlib import Path


class WebAction(CustomWait):

    def __init__(self, driver, model, timeout=30):
        super().__init__(timeout)
        self._driver = driver
        self._model = model
        self._config = LoadConfig()
        self._img = Path(__file__).absolute().parent.parent.joinpath("resource", "img", f"{self._config['img']}.png")

    def wait_until_text_display(self, text):
        self.until(TextDisplayOnPage(text, self._img), f"cannot see --{text}-- on page")

    def wait_until_element_display(self, element, keyword):
        pass
