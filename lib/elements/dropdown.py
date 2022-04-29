from lib.elements.base import ElementBase


class Dropdown(ElementBase):
    
    def __init__(self, keyword=None, direction=None):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.element_type = self.__class__.__mro__[-3].__qualname__

    def select_item(self, name, *args):
        dropdown = self.wait_element_visible()
        self.action_click(dropdown)
        item = self._action.common_option_legacy_element(name)
        if item:
            item.click()
        else:
            self.action_send_value(dropdown, name.lower())
            self.action_press_key(dropdown, "enter")

    def click(self, *args):
        dropdown = self.wait_element_visible()
        self.action_click(dropdown)
