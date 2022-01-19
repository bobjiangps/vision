from lib.non_ai_elements.base import NonAiElementBase


class NonAiStatic(NonAiElementBase):

    def __call__(self, identify_type, identify_value):
        self.identify_type = identify_type
        self.identify_value = identify_value
        return self._produce()

    def click(self):
        static = self.wait_element_visible()
        # static.click()
        self.action_click(static)

    def input(self, value):
        static = self.wait_element_visible()
        # static.send_keys(value)
        self.action_input(static, value)
