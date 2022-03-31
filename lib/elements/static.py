from lib.elements.base import ElementBase


class Static(ElementBase):

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.element_type = self.__class__.__mro__[-3].__qualname__
        self.beyond = False

    def click(self, *args):
        element = self.wait_element_visible()
        self.action_click(element)

    def input(self, value, *args):
        element = self.wait_element_visible()
        self.action_input(element, value)
