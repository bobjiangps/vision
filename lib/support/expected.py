from lib.visual.imager import Imager
from lib.visual.common import center, proportion, distance_by_direction
from lib.support.exceptions import NotVisibleException
from lib.visual.pred import predict
from pathlib import Path
from conf.config import LoadConfig


class BaseExpectation:

    def __init__(self):
        self._img = str(Path.cwd().joinpath("resource", "img", f"{LoadConfig().model['img']}.png"))

    @staticmethod
    def get_viewport_size(driver):
        width = driver.execute_script("return window.innerWidth;")
        height = driver.execute_script("return window.innerHeight;")
        return [width, height]

    @staticmethod
    def get_body_size(driver):
        body = driver.find_element_by_tag_name("body")
        size = body.size
        return [size["width"], size["height"]]


class TextDisplayOnPage(BaseExpectation):

    def __init__(self, text):
        super().__init__()
        self.text = text

    def __call__(self, driver):
        driver.save_screenshot(self._img)
        contours, shape = Imager.recognize_contours(self._img)
        for t in self.text.split("|"):
            for c in contours:
                if c[1].find(t.strip()) >= 0:
                    return proportion(center(c[0]), self.get_viewport_size(driver), shape)
        words = []
        double_check = False
        for t in self.text.split("|"):
            if t.find(" ") > 0:
                words.append(t.split(" ")[0])
        for w in words:
            if str(contours).find(f"'{w}'") > 0:
                double_check = True
                break
        if double_check:
            contours, shape = Imager.recognize_contours(self._img, font="large")
            for t in self.text.split("|"):
                for c in contours:
                    if c[1].find(t.strip()) >= 0:
                        return proportion(center(c[0]), self.get_viewport_size(driver), shape)
        # raise NotVisibleException("text NOT visible")
        return False


class ElementDisplayOnPage(BaseExpectation):

    def __init__(self, model, element, keyword=None):
        super().__init__()
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
                        if Imager.recognize_crop_contours(self._img, r["COOR"]).find(k.strip()) >= 0:
                            return proportion(center(r["COOR"]), self.get_viewport_size(driver), shape)
                else:
                    return proportion(center(r["COOR"]), self.get_viewport_size(driver), shape)
        # raise NotVisibleException("text NOT visible")
        return False


class ElementMatchOnPage(BaseExpectation):

    def __init__(self, model, element, keyword, direction):
        super().__init__()
        self.model = model
        self.element = element.lower()
        self.keyword = keyword
        self.direction = direction.lower() if direction else "down"

    def __call__(self, driver):
        driver.save_screenshot(self._img)
        match_keyword = None
        match_area = None
        contours, shape = Imager.recognize_contours(self._img)
        for c in contours:
            for t in self.keyword.split("|"):
                if c[1].find(t.strip()) >= 0:
                    match_keyword = proportion(center(c[0]), self.get_viewport_size(driver), shape)
                    match_area = c[0]
                    break
        if not match_keyword:
            return False
        results, labels, shape = predict(self.model)
        if self.element not in labels.keys():
            return False
        relative_elements = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "nearby": []
        }
        for r in results:
            if r["N"] == self.element:
                if r["COOR"][3] < match_area[3] and r["COOR"][1] < match_area[1]:
                    relative_elements["up"].append(r["COOR"])
                elif r["COOR"][3] > match_area[3] and r["COOR"][1] > match_area[1]:
                    relative_elements["down"].append(r["COOR"])
                elif r["COOR"][2] < match_area[2] and r["COOR"][0] < match_area[0]:
                    relative_elements["left"].append(r["COOR"])
                elif r["COOR"][2] > match_area[2] and r["COOR"][0] > match_area[0]:
                    relative_elements["right"].append(r["COOR"])
                else:
                    relative_elements["nearby"].append(r["COOR"])
        matched_element = None
        distance = None
        for e in relative_elements[self.direction]:
            position = proportion(center(e), self.get_viewport_size(driver), shape)
            if not matched_element:
                distance = (position[0] - match_keyword[0]) ** 2 + (position[1] - match_keyword[1]) ** 2
                matched_element = position
            else:
                temp = (position[0] - match_keyword[0]) ** 2 + (position[1] - match_keyword[1]) ** 2
                if temp < distance:
                    matched_element = position
                    distance = temp
        return matched_element
