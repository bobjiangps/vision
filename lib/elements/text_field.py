from lib.elements.base import ElementBase
import re


class TextField(ElementBase):

    element_type = "_".join(re.findall("[A-Z][^A-Z]*", __qualname__))

    def __call__(self, keyword=None):
        self.keyword = keyword
        return self

    def input(self, value):
        if self.keyword:
            text_field = self.wait_element_match_visible(element=self.element_type, keyword=self.keyword)
        else:
            text_field = self.wait_element_visible(element=self.element_type)
        self.action_input(text_field, value)
