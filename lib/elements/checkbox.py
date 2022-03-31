from lib.elements.base import ElementBase


class Checkbox(ElementBase):

    def __init__(self, keyword=None, direction="Left"):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.element_type = self.__class__.__mro__[-3].__qualname__

    def check(self, *args):
        # todo: uncheck and is_checked are not ready
        checkbox = self.wait_element_visible()
        self.action_click(checkbox)
