from utils.image_processor import ImageProcessor as IP
from common.support.exceptions import NotVisibleException


class TextDisplayOnPage:

    def __init__(self, text, img):
        self.text = text
        self.img = img

    def __call__(self):
        contours = IP.recognize_contours(self.img)
        for c in contours:
            if c[1].find(self.text) >= 0:
                return c[0]
        raise NotVisibleException()
