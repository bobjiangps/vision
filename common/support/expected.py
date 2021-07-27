from utils.image_processor import ImageProcessor as IP
from common.support.exceptions import NotVisibleException
from models.pred import predict
from pathlib import Path
from conf.config import LoadConfig
from utils.general import center, proportion


class BaseExpectation:

    def __init__(self):
        self._img = str(Path.cwd().joinpath("resource", "img", f"{LoadConfig().model['img']}.png"))

    @staticmethod
    def get_viewport_size(driver):
        width = driver.execute_script("return window.innerWidth;")
        height = driver.execute_script("return window.innerHeight;")
        return [width, height]


class TextDisplayOnPage(BaseExpectation):

    def __init__(self, text):
        super(TextDisplayOnPage, self).__init__()
        self.text = text

    def __call__(self, driver):
        driver.save_screenshot(self._img)
        contours, shape = IP.recognize_contours(self._img)
        for c in contours:
            if c[1].find(self.text) >= 0:
                return proportion(center(c[0]), self.get_viewport_size(driver), shape)
        # raise NotVisibleException("text NOT visible")
        return False


class ElementDisplayOnPage(BaseExpectation):

    def __init__(self, model, element, keyword=None):
        super(ElementDisplayOnPage, self).__init__()
        self.model = model
        self.element = element.lower()
        self.keyword = keyword

    def __call__(self, driver):
        driver.save_screenshot(self._img)
        results, labels, shape = predict(self.model)
        if self.element not in labels.keys():
            return False
        for r in results:
            if r["N"] == self.element:
                if self.keyword:
                    for k in self.keyword.split("|"):
                        if IP.recognize_crop_contours(self._img, r["COOR"]).find(k.strip()) >= 0:
                            return proportion(center(r["COOR"]), self.get_viewport_size(driver), shape)
                else:
                    return proportion(center(r["COOR"]), self.get_viewport_size(driver), shape)
        # raise NotVisibleException("text NOT visible")
        return False
