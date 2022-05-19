from lib.elements.base import ElementBase
import re


class RadioButton(ElementBase):
    
    def __init__(self, keyword=None, direction="Left", refer=None):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.refer = refer
        self.element_type = "_".join(re.findall("[A-Z][^A-Z]*", self.__class__.__mro__[-3].__qualname__))

    def select(self, *args):
        # todo: unselect and is_selected are not ready
        radio_button = self.wait_element_visible()
        self.action_click(radio_button)
