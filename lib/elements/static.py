from selenium.webdriver.common.action_chains import ActionChains
from lib.elements.base import ElementBase


class Static(ElementBase):

    element_type = "Static"

    def __call__(self, text):
        self.text = text
        return self

    def input(self, value):
        element = self.wait_text_visible(text=self.text)
        body = self._driver.find_element_by_tag_name("body")
        ActionChains(self._driver).move_to_element_with_offset(body, element[0], element[1] + self._offset[1]).click().send_keys(value).perform()
