from lib.elements.base import ElementBase


class Dropdown(ElementBase):
    
    def __init__(self, keyword=None, direction=None):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.element_type = self.__class__.__mro__[-3].__qualname__

    def select_item(self, name):
        dropdown = self.wait_element_match_visible()
        self.action_input(dropdown, name)
        self.action_press_key(dropdown, "enter")
