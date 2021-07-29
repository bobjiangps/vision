from selenium.webdriver.common.action_chains import ActionChains


class ElementBase:

    def __init__(self, driver, action, offset):
        self._driver = driver
        self._action = action
        self._offset = offset
        self.action_chains = ActionChains(self._driver)

    def wait_text_visible(self, **kwargs):
        return self._action.wait_until_text_display(kwargs["text"])

    def wait_element_visible(self, **kwargs):
        return self._action.wait_until_element_display(kwargs["element"], kwargs.get("keyword", None))

    def wait_element_match_visible(self, **kwargs):
        return self._action.wait_until_element_match(kwargs["element"], kwargs["keyword"])

    def action_click(self, element):
        body = self._driver.find_element_by_tag_name("body")
        self.action_chains.move_to_element_with_offset(body, element[0],
                                                       element[1] + self._offset[1]).click().perform()

    def action_input(self, element, value):
        body = self._driver.find_element_by_tag_name("body")
        self.action_chains.move_to_element_with_offset(body, element[0],
                                                       element[1] + self._offset[1]).click().send_keys(value).perform()
