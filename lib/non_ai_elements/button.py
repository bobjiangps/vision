from lib.non_ai_elements.base import NonAiElementBase


class NonAiButton(NonAiElementBase):

    def __call__(self, identify_type, identify_value):
        self.identify_type = identify_type
        self.identify_value = identify_value
        return self

    def click(self):
        btn = self.wait_element_clickable()
        # btn.click()
        self.action_click(btn)
