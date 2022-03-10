from lib.elements.base import ElementBase


class Button(ElementBase):

    def __init__(self, keyword=None):
        super().__init__()
        self.keyword = keyword
        self.element_type = self.__class__.__base__.__qualname__
        self.beyond = False

    def click(self):
        btn = self.wait_element_visible()
        self.action_click(btn)
