from lib.non_ai_elements.base import NonAiElementBase


class NonAiButton(NonAiElementBase):

    def click(self):
        btn = self.wait_element_clickable()
        # btn.click()
        self.action_click(btn)
