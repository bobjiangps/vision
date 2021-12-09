from lib.non_ai_elements.base import NonAiElementBase


class NonAiTextField(NonAiElementBase):

    def __call__(self, identify_type, identify_value):
        self.identify_type = identify_type
        self.identify_value = identify_value
        return self

    def input(self, value):
        text_field = self.wait_element_visible()
        # text_field.send_keys(value)
        self.action_input(text_field, value)
