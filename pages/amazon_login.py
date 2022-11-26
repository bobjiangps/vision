from lib.test_base.page_base import *


class AmazonLogin(PageBase):

    def __init__(self):
        super().__init__()
        self.sign_in_button = Button("Sign in")
        self.sign_in_text_field = TextField("Sign in")
        self.continue_button = Button("Continue")
        self.username_not_found_err_msg = Static("We cannot find an account with that email address")
        self.username_not_input_err_msg = Static("Enter your email or mobile phone")

    def go_to_main_page(self):
        self.browse_page("https://www.amazon.com/?language=en_US")
        self.sign_in_button.wait_element_visible()
        return self

    def navigate_to_signin_page(self):
        self.sign_in_button.click()
        self.continue_button.wait_element_visible()
        return self

    def continue_without_input_username(self):
        self.continue_button.click()
        return self

    def input_username_to_continue(self, value):
        self.sign_in_text_field.input(value)
        self.continue_button.click()
        return self
