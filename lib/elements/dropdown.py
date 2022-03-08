from lib.elements.base import ElementBase
from lib.elements.static import Static


class Dropdown(ElementBase):
    
    def __init__(self, keyword=None, direction=None):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.element_type = self.__class__.__qualname__

    def select_item(self, item_name):
        dropdown = self.wait_element_match_visible()
        self.action_click(dropdown)
        item = Static(item_name).wait_text_visible()
        self.action_click(item)
