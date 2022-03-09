from lib.elements.base import ElementBase


class Static(ElementBase):

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.element_type = self.__class__.__base__.__qualname__

    def click(self):
        element = self.wait_text_visible()
        self.action_click(element)

    def input(self, value):
        element = self.wait_text_visible()
        self.action_input(element, value)
