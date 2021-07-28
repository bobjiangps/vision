from selenium.webdriver.common.action_chains import ActionChains
from lib.elements.base import ElementBase


class Button(ElementBase):

    element_type = "Button"

    def __call__(self, keyword=None):
        self.keyword = keyword
        return self

    def click(self):
        btn = self.wait_element_visible(element=self.element_type, keyword=self.keyword)
        body = self._driver.find_element_by_tag_name("body")
        ActionChains(self._driver).move_to_element_with_offset(body, btn[0], btn[1] + self._offset[1]).click().perform()
