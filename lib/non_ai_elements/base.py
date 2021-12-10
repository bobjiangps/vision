class NonAiElementBase:

    def __init__(self, action):
        self._action = action
        self.identify_type = None
        self.identify_value = None

    def element(self):
        return self._action.find_non_ai_element(self.identify_type, self.identify_value)

    def elements(self):
        return self._action.find_non_ai_elements(self.identify_type, self.identify_value)

    def wait_element_present(self):
        return self._action.wait_until_non_ai_element_present(self.identify_type, self.identify_value)

    def wait_element_visible(self):
        return self._action.wait_until_non_ai_element_display(self.identify_type, self.identify_value)

    def wait_element_disappear(self):
        return self._action.wait_until_non_ai_element_disappear(self.identify_type, self.identify_value)

    def wait_element_clickable(self):
        return self._action.wait_until_non_ai_element_clickable(self.identify_type, self.identify_value)

    def wait_element_selected(self):
        return self._action.wait_until_non_ai_element_selected(self.identify_type, self.identify_value)

    def action_click(self, element):
        self._action.click_non_ai_element(element)

    def action_input(self, element, value):
        self._action.input_non_ai_element(element, value)
