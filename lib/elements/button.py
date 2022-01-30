from lib.elements.base import ElementBase


class Button(ElementBase):

    def __init__(self, keyword=None):
        super().__init__()
        self.keyword = keyword
        self.element_type = self.__class__.__qualname__

    def click(self):
        btn = self.wait_element_visible()
        self.action_click(btn)
