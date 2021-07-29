from lib.elements.base import ElementBase


class Static(ElementBase):

    element_type = __qualname__

    def __call__(self, text):
        self.text = text
        return self

    def click(self):
        element = self.wait_text_visible(text=self.text)
        self.action_click(element)

    def input(self, value):
        element = self.wait_text_visible(text=self.text)
        self.action_input(element, value)
