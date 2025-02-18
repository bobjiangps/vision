from lib.elements.base import ElementBase
import re


class TextField(ElementBase):

    def __init__(self, keyword=None, direction=None, refer=None):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.refer = refer
        self.element_type = "_".join(re.findall("[A-Z][^A-Z]*", self.__class__.__mro__[-3].__qualname__))

    def input(self, value, *args):
        text_field = self.wait_element_visible()
        self.action_input(text_field, value)

    def clear(self, *args):
        text_field = self.wait_element_visible()
        self.action_clear(text_field)
