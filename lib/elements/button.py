from lib.elements.base import ElementBase


class Button(ElementBase):

    def __init__(self, keyword=None, refer=None):
        super().__init__()
        self.keyword = keyword
        self.refer = refer
        self.element_type = self.__class__.__mro__[-3].__qualname__
        self.beyond = False

    def click(self, *args):
        btn = self.wait_element_visible()
        self.action_click(btn)
