from lib.elements.base import ElementBase
import re


class TextField(ElementBase):

    def __init__(self, keyword=None, direction=None):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.element_type = "_".join(re.findall("[A-Z][^A-Z]*", self.__class__.__qualname__))

    def input(self, value):
        text_field = self.wait_element_match_visible()
        self.action_input(text_field, value)
