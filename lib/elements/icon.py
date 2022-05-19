from lib.elements.base import ElementBase


class Icon(ElementBase):

    def __init__(self, category, keyword=None, refer=None):
        super().__init__()
        self.element_type = self.__class__.__mro__[-3].__qualname__
        self.category = category
        if not keyword:
            self.beyond = False
        else:
            self.keyword = keyword
        self.refer = refer

    def click(self, *args):
        icon = self.wait_element_visible()
        self.action_click(icon)
