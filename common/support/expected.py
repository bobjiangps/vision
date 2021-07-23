from utils.image_processor import ImageProcessor as IP
from common.support.exceptions import NotVisibleException
from pathlib import Path
from conf.config import LoadConfig


class BaseExpectation:

    def __init__(self):
        self._img = str(Path.cwd().joinpath("resource", "img", f"{LoadConfig().model['img']}.png"))


class TextDisplayOnPage(BaseExpectation):

    def __init__(self, text):
        super(TextDisplayOnPage, self).__init__()
        self.text = text

    def __call__(self):
        contours = IP.recognize_contours(self._img)
        for c in contours:
            if c[1].find(self.text) >= 0:
                return c[0]
        raise NotVisibleException("text NOT visible")
