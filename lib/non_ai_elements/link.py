from lib.non_ai_elements.base import NonAiElementBase


class NonAiLink(NonAiElementBase):

    def click(self):
        link = self.wait_element_visible()
        # link.click()
        self.action_click(link)
