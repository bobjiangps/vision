from lib.elements.base import ElementBase
import re


class RadioButton(ElementBase):
    
    def __init__(self, keyword=None, direction="Left"):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.element_type = "_".join(re.findall("[A-Z][^A-Z]*", self.__class__.__qualname__))

    def select(self):
        # todo: unselect and is_selected are not ready
        radio_button = self.wait_element_match_visible()
        self.action_click(radio_button)
