from lib.elements.base import ElementBase
import re


class TextField(ElementBase):

    def __call__(self, keyword=None):
        self.keyword = keyword
        self.element_type = "_".join(re.findall("[A-Z][^A-Z]*", self.__class__.__qualname__))
        return self._produce()

    def input(self, value):
        text_field = self.wait_element_match_visible()
        self.action_input(text_field, value)
