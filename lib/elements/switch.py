from lib.elements.base import ElementBase


class Switch(ElementBase):

    def __init__(self, keyword=None, direction=None, ref_name=None):
        super().__init__()
        self.keyword = keyword
        self.direction = direction
        self.ref_name = ref_name
        self.element_type = self.__class__.__mro__[-3].__qualname__

    def click(self, *args):
        btn = self.wait_element_visible()
        self.action_click(btn)
