from lib.elements.base import ElementBase


class Button(ElementBase):

    element_type = "Button"

    def __call__(self, keyword=None):
        self.keyword = keyword
        return self

    def click(self):
        btn = self.wait_element_visible(element=self.element_type, keyword=self.keyword)
        self.action_click(btn)
