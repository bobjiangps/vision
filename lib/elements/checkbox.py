from lib.elements.base import ElementBase


class Checkbox(ElementBase):

    def __init__(self, keyword=None, direction="Left"):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.element_type = self.__class__.__base__.__qualname__

    def check(self):
        # todo: uncheck and is_checked are not ready
        checkbox = self.wait_element_match_visible()
        self.action_click(checkbox)
