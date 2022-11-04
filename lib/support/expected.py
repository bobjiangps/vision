from lib.visual.imager import Imager
from lib.visual.common import center, proportion
from lib.support.exceptions import NotVisibleException
from lib.visual.pred import predict
from lib.support.deviation import *
from conf.config import LoadConfig
from pathlib import Path
import json
import base64


class BaseExpectation:

    FULL_SCREEN = False

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

    def save_full_screenshot(self, driver):
        def send(cmd, params):
            resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
            url = driver.command_executor._url + resource
            body = json.dumps({"cmd":cmd, "params": params})
            response = driver.command_executor._request("POST", url, body)
            return response.get("value")

        def evaluate(script):
            response = send("Runtime.evaluate", {"returnByValue": True, "expression": script})
            return response["result"]["value"]

        if hasattr(driver, "get_full_page_screenshot_as_file"):
            driver.get_full_page_screenshot_as_file(self._img)
        else:
            if driver.name.lower() == "chrome":
                metrics = evaluate(
                    "({" + \
                    "width: Math.max(window.innerWidth, document.body.scrollWidth, document.documentElement.scrollWidth)|0," + \
                    "height: Math.max(innerHeight, document.body.scrollHeight, document.documentElement.scrollHeight)|0," + \
                    "deviceScaleFactor: window.devicePixelRatio || 1," + \
                    "mobile: typeof window.orientation !== 'undefined'" + \
                    "})")
                send("Emulation.setDeviceMetricsOverride", metrics)
                screenshot = send("Page.captureScreenshot", {"format": "png", "fromSurface": True})
                send("Emulation.clearDeviceMetricsOverride", {})
                with open(self._img, 'wb') as f:
                    f.write(base64.b64decode(screenshot['data']))
            elif driver.name.lower() == "firefox":
                resource = "/session/%s/moz/screenshot/full" % driver.session_id
                url = driver.command_executor._url + resource
                content = driver.command_executor._request("GET", url)
                with open(self._img, 'wb') as f:
                    f.write(base64.b64decode(content["value"]))
            else:
                driver.save_screenshot(self._img)

    @staticmethod
    def scroll_into_view(driver, position):
        driver.execute_script(f"window.scrollTo({position[0]}, {position[1]});")


class TextDisplayOnPage(BaseExpectation):

    def __init__(self, text, multiple=False):
        super().__init__()
        self.text = text
        self.multiple = multiple
        self.elements = []

    def __call__(self, driver):
        if self.FULL_SCREEN:
            self.save_full_screenshot(driver)
        else:
            driver.save_screenshot(self._img)
        contours, shape = Imager.recognize_contours(self._img)
        for t in self.text.split("|"):
            for c in contours:
                found = c[1].find(t.strip()) >= 0
                if found or qualified(c[1], t):
                    if self.FULL_SCREEN:
                        self.FULL_SCREEN = False
                        self.scroll_into_view(driver, proportion(center(c[0]), self.get_body_size(driver), shape))
                        return False
                    else:
                        if found:
                            accurate_c = [p for p in c[0]]
                            width = c[0][2] - c[0][0]
                            if c[1].find(self.text.strip()) / len(c[1]) > 0.2:
                                accurate_c[0] += width * (c[1].find(self.text.strip()) / len(c[1]))
                            if (c[1].find(self.text.strip()) + len(self.text.strip())) / len(c[1]) < 0.8:
                                accurate_c[2] = c[0][0] + width * ((c[1].find(self.text.strip()) + len(self.text.strip())) / len(c[1]))
                        else:
                            accurate_c = c[0]
                        if self.multiple:
                            self.elements.append(proportion(center(accurate_c), self.get_viewport_size(driver), shape))
                        else:
                            return proportion(center(accurate_c), self.get_viewport_size(driver), shape)
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
                    if c[1].find(t.strip()) >= 0 or qualified(c[1], t):
                        if self.FULL_SCREEN:
                            self.FULL_SCREEN = False
                            self.scroll_into_view(driver, proportion(center(c[0]), self.get_body_size(driver), shape))
                            return False
                        else:
                            if self.multiple:
                                self.elements.append(proportion(center(c[0]), self.get_viewport_size(driver), shape))
                            else:
                                return proportion(center(c[0]), self.get_viewport_size(driver), shape)
        self.FULL_SCREEN = True
        # raise NotVisibleException("text NOT visible")
        if len(self.elements) > 0:
            return self.elements
        return False


class ElementDisplayOnPage(BaseExpectation):

    def __init__(self, model, element, keyword=None, multiple=False):
        super().__init__()
        self.model = model
        self.element = element.lower()
        self.keyword = keyword
        self.multiple = multiple
        self.elements = []

    def __call__(self, driver):
        if self.FULL_SCREEN:
            self.save_full_screenshot(driver)
        else:
            driver.save_screenshot(self._img)
        results, labels, shape = predict(self.model)
        if self.element not in labels.keys():
            return False
        for r in results:
            if r["N"] == self.element:
                if self.keyword:
                    tmp = Imager.recognize_crop_contours(self._img, r["COOR"])
                    for k in self.keyword.split("|"):
                        if not tmp:
                            (x, y) = proportion(center(r["COOR"]), self.get_viewport_size(driver), shape)
                            tmp = driver.execute_script(f"return document.elementFromPoint({x}, {y});").text
                            if tmp.find("\n") > 0:
                                continue
                        if tmp.find(k.strip()) >= 0 or qualified(tmp, k):
                            if self.FULL_SCREEN:
                                self.FULL_SCREEN = False
                                self.scroll_into_view(driver, proportion(center(r["COOR"]), self.get_body_size(driver), shape))
                                return False
                            else:
                                if self.multiple:
                                    self.elements.append(proportion(center(r["COOR"]), self.get_viewport_size(driver), shape))
                                else:
                                    return proportion(center(r["COOR"]), self.get_viewport_size(driver), shape)
                else:
                    if self.FULL_SCREEN:
                        self.FULL_SCREEN = False
                        self.scroll_into_view(driver, proportion(center(r["COOR"]), self.get_body_size(driver), shape))
                        return False
                    else:
                        if self.multiple:
                            self.elements.append(proportion(center(r["COOR"]), self.get_viewport_size(driver), shape))
                        else:
                            return proportion(center(r["COOR"]), self.get_viewport_size(driver), shape)
        self.FULL_SCREEN = True
        # raise NotVisibleException("text NOT visible")
        if len(self.elements) > 0:
            return self.elements
        return False


class ElementMatchOnPage(BaseExpectation):

    def __init__(self, model, element, keyword, direction, multiple=False):
        super().__init__()
        self.model = model
        self.element = element.lower()
        self.keyword = keyword
        self.direction = direction.lower() if direction else "down"
        self.multiple = multiple
        self.elements = []

    def __call__(self, driver):
        if self.FULL_SCREEN:
            self.save_full_screenshot(driver)
        else:
            driver.save_screenshot(self._img)
        match_keyword = None
        match_area = None
        contours, shape = Imager.recognize_contours(self._img)
        exit_flag = False
        for c in contours:
            for t in self.keyword.split("|"):
                if c[1].find(t.strip()) >= 0 or qualified(c[1], t):
                    if self.FULL_SCREEN:
                        self.FULL_SCREEN = False
                        self.scroll_into_view(driver, proportion(center(c[0]), self.get_body_size(driver), shape))
                        return False
                    match_keyword = proportion(center(c[0]), self.get_viewport_size(driver), shape)
                    match_area = c[0]
                    exit_flag = True
                    break
            if exit_flag:
                break
        if not match_keyword:
            self.FULL_SCREEN = True
            return False
        results, labels, shape = predict(self.model)
        if self.element not in labels.keys():
            self.FULL_SCREEN = True
            return False
        relative_elements = {
            "up": {"area": [], "edge": [], "orientation": [], "match_orien": (match_area[0], match_area[2])},
            "down": {"area": [], "edge": [], "orientation": [], "match_orien": (match_area[0], match_area[2])},
            "left": {"area": [], "edge": [], "orientation": [], "match_orien": (match_area[1], match_area[3])},
            "right": {"area": [], "edge": [], "orientation": [], "match_orien": (match_area[1], match_area[3])}
        }
        for r in results:
            if r["N"] == self.element:
                if r["COOR"][3] < match_area[3] and r["COOR"][1] < match_area[1]:
                    relative_elements["up"]["area"].append(r["COOR"])
                    relative_elements["up"]["edge"].append((r["COOR"][0], r["COOR"][3], r["COOR"][2], r["COOR"][3]))
                    relative_elements["up"]["orientation"].append((r["COOR"][0], r["COOR"][2]))
                if r["COOR"][3] > match_area[3] and r["COOR"][1] > match_area[1]:
                    relative_elements["down"]["area"].append(r["COOR"])
                    relative_elements["down"]["edge"].append((r["COOR"][0], r["COOR"][1], r["COOR"][2], r["COOR"][1]))
                    relative_elements["down"]["orientation"].append((r["COOR"][0], r["COOR"][2]))
                if r["COOR"][2] < match_area[2] and r["COOR"][0] < match_area[0]:
                    relative_elements["left"]["area"].append(r["COOR"])
                    relative_elements["left"]["edge"].append((r["COOR"][2], r["COOR"][1], r["COOR"][2], r["COOR"][3]))
                    relative_elements["left"]["orientation"].append((r["COOR"][1], r["COOR"][3]))
                if r["COOR"][2] > match_area[2] and r["COOR"][0] > match_area[0]:
                    relative_elements["right"]["area"].append(r["COOR"])
                    relative_elements["right"]["edge"].append((r["COOR"][0], r["COOR"][1], r["COOR"][0], r["COOR"][3]))
                    relative_elements["right"]["orientation"].append((r["COOR"][1], r["COOR"][3]))
        matched_element = None
        distance = None
        for inx, e in enumerate(relative_elements[self.direction]["edge"]):
            if (relative_elements[self.direction]["match_orien"][0] > relative_elements[self.direction]["orientation"][inx][1]) or (relative_elements[self.direction]["match_orien"][1] < relative_elements[self.direction]["orientation"][inx][0]):
                continue
            else:
                position = proportion(center(e), self.get_viewport_size(driver), shape)
                if not matched_element:
                    distance = (position[0] - match_keyword[0]) ** 2 + (position[1] - match_keyword[1]) ** 2
                    matched_element = proportion(center(relative_elements[self.direction]["area"][inx]), self.get_viewport_size(driver), shape)
                    if self.multiple:
                        self.elements.append(matched_element)
                else:
                    temp = (position[0] - match_keyword[0]) ** 2 + (position[1] - match_keyword[1]) ** 2
                    if temp < distance:
                        matched_element = proportion(center(relative_elements[self.direction]["area"][inx]), self.get_viewport_size(driver), shape)
                        distance = temp
                        if self.multiple:
                            self.elements.insert(0, matched_element)
                    else:
                        if self.multiple:
                            matched_element = proportion(center(relative_elements[self.direction]["area"][inx]), self.get_viewport_size(driver), shape)
                            self.elements.append(matched_element)
        if not matched_element:
            for inx, e in enumerate(relative_elements[self.direction]["edge"]):
                position = proportion(center(e), self.get_viewport_size(driver), shape)
                if not matched_element:
                    distance = (position[0] - match_keyword[0]) ** 2 + (position[1] - match_keyword[1]) ** 2
                    matched_element = proportion(center(relative_elements[self.direction]["area"][inx]), self.get_viewport_size(driver), shape)
                    if self.multiple:
                        self.elements.append(matched_element)
                else:
                    temp = (position[0] - match_keyword[0]) ** 2 + (position[1] - match_keyword[1]) ** 2
                    if temp < distance:
                        matched_element = proportion(center(relative_elements[self.direction]["area"][inx]), self.get_viewport_size(driver), shape)
                        distance = temp
                        if self.multiple:
                            self.elements.insert(0, matched_element)
                    else:
                        if self.multiple:
                            matched_element = proportion(center(relative_elements[self.direction]["area"][inx]), self.get_viewport_size(driver), shape)
                            self.elements.append(matched_element)
        self.FULL_SCREEN = False
        if len(self.elements) > 0:
            return self.elements
        return matched_element


class ElementByRegionDisplayOnPage(BaseExpectation):
    # incomplete

    def __init__(self, model, element, refer, keyword=None, multiple=False):
        super().__init__()
        self.model = model
        self.element = element.lower()
        self.refer = refer
        self.keyword = keyword
        self.text = keyword if self.element in ["static"] else None
        self.multiple = multiple
        self.elements = []

    def __call__(self, driver):
        if self.FULL_SCREEN:
            self.save_full_screenshot(driver)
        else:
            driver.save_screenshot(self._img)
        refer_position = None
        contours, shape = Imager.recognize_contours(self._img)
        for c in contours:
            if c[1].find(self.refer) >= 0 or qualified(c[1], self.refer):
                if self.FULL_SCREEN:
                    self.FULL_SCREEN = False
                    self.scroll_into_view(driver, proportion(center(c[0]), self.get_body_size(driver), shape))
                    return False
                else:
                    refer_position = proportion(center(c[0]), self.get_viewport_size(driver), shape)
                    break
        if not refer_position:
            self.FULL_SCREEN = True
            return False
        else:
            regions = Imager.recognize_region(self._img)
            elements = ElementDisplayOnPage(self.model, self.element, self.keyword, True)(driver)
            matched_elements = []
            for r in regions:
                proportion_r_left_top = proportion((r[0], r[1]), self.get_viewport_size(driver), shape)
                proportion_r_right_bottom = proportion((r[2], r[3]), self.get_viewport_size(driver), shape)
                proportion_r = (proportion_r_left_top[0], proportion_r_left_top[1], proportion_r_right_bottom[0], proportion_r_right_bottom[1])
                if proportion_r[0] < refer_position[0] < proportion_r[2] and proportion_r[1] < refer_position[1] < proportion_r[3]:
                    for e in elements:
                        if proportion_r[0] < e[0] < proportion_r[2] and proportion_r[1] < e[1] < proportion_r[3]:
                            matched_elements.append(e)
            if len(matched_elements) > 0:
                if self.multiple:
                    return matched_elements
                else:
                    return matched_elements[0]
            else:
                return False

# class ElementByRegionDisplayOnPage(BaseExpectation):
#     # incomplete
#
#     def __init__(self, model, element, refer, keyword=None, multiple=False):
#         super().__init__()
#         self.model = model
#         self.element = element.lower()
#         self.refer = refer
#         self.keyword = keyword
#         self.text = keyword if self.element in ["static"] else None
#         self.multiple = multiple
#         self.elements = []
#
#     def __call__(self, driver):
#         if self.FULL_SCREEN:
#             self.save_full_screenshot(driver)
#         else:
#             driver.save_screenshot(self._img)
#         refer_position = None
#         contours, shape = Imager.recognize_contours(self._img)
#         for c in contours:
#             if c[1].find(self.refer) >= 0 or qualified(c[1], self.refer):
#                 if self.FULL_SCREEN:
#                     self.FULL_SCREEN = False
#                     self.scroll_into_view(driver, proportion(center(c[0]), self.get_body_size(driver), shape))
#                     return False
#                 else:
#                     refer_position = proportion(center(c[0]), self.get_viewport_size(driver), shape)
#                     break
#         if not refer_position:
#             self.FULL_SCREEN = True
#             return False
#         else:
#             texts_y_in_column = []
#             refer_js_rect = driver.execute_script(f"return document.elementFromPoint({refer_position[0]}, {refer_position[1]}).getClientRects()[0];")
#             for c in contours:
#                 temp_position = proportion(center(c[0]), self.get_viewport_size(driver), shape)
#                 temp_js_rect = driver.execute_script(f"return document.elementFromPoint({temp_position[0]}, {temp_position[1]}).getClientRects()[0];")
#                 if refer_js_rect["left"] == temp_js_rect["left"] and refer_js_rect["height"] == temp_js_rect["height"]:
#                     texts_y_in_column.append(temp_js_rect["y"])
#             texts_y_in_column.sort()
#             amounts = len(texts_y_in_column)
#             y_range = ()
#             if amounts > 1:
#                 for inx, y in enumerate(texts_y_in_column):
#                     if y == refer_js_rect["y"]:
#                         if inx == (amounts - 1):
#                             y_range = (y-20, self.get_viewport_size(driver)[1])
#                         else:
#                             y_range = (y-20, texts_y_in_column[inx+1]-20)
#                 if self.text is not None:
#                     temp_elements = TextDisplayOnPage(self.text, multiple=True)(driver)
#                 else:
#                     temp_elements = ElementDisplayOnPage(self.model, self.element, self.keyword, multiple=True)(driver)
#                 if temp_elements:
#                     elements_by_region = []
#                     for e in temp_elements:
#                         if y_range[0] <= e[1] <= y_range[1]:
#                             if self.multiple:
#                                 elements_by_region.append(e)
#                             else:
#                                 return e
#                     return elements_by_region
#                 else:
#                     return False
#             else:
#                 if self.text:
#                     return TextDisplayOnPage(self.text, self.multiple)(driver)
#                 else:
#                     return ElementDisplayOnPage(self.model, self.element, self.keyword, self.multiple)(driver)
