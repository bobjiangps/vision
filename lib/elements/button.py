from lib.elements.base import ElementBase


class Button(ElementBase):

    def __call__(self, keyword=None):
        self.keyword = keyword
        self.element_type = self.__class__.__qualname__
        return self._produce()

    def click(self):
        btn = self.wait_element_visible()
        self.action_click(btn)
