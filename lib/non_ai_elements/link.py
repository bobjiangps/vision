from lib.non_ai_elements.base import NonAiElementBase


class NonAiLink(NonAiElementBase):

    def __call__(self, identify_type, identify_value):
        self.identify_type = identify_type
        self.identify_value = identify_value
        return self

    def click(self):
        link = self.wait_element_visible()
        # link.click()
        self.action_click(link)
