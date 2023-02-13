from lib.test_base.page_base import *
from pages.stackoverflow_signup import StackoverflowSignup


class StackoverflowLogin(PageBase):

    def __init__(self):
        super().__init__()
        self.accept_cookie_btn = Button("Accept all cookies")
        self.sign_up_btn = Button("Sign up")
        self.sign_in_button = Button("Log  in")
        self.email_err_msg = Static("Email cannot be empty")
        self.password_err_msg = Static("Password cannot be empty")
        self.retry_source_msg = Static("Retry using another source")

    def check_source_message(self):
        self.sign_up_btn.wait_element_visible()
        if self.retry_source_msg.is_visible():
            self.retry_source_msg.click()
            self.sign_up_btn.wait_element_visible()

    def go_to_login_page_and_accept_cookie(self):
        self.browse_page("https://stackoverflow.com/users/login")
        self.accept_cookie_btn.click()
        # self.accept_cookie_btn.wait_element_invisible()  # in chine, always load js fail, click on it but cannot make it disappear
        return self

    def login_without_input_anything(self):
        ele = self.sign_in_button.elements()
        if len(ele) > 1:
            self.log.info("multiple elements found")
            self.action.click(ele[-1])
        else:
            self.sign_in_button.click()
        return self

    def navigate_to_signup_page(self):
        self.sign_up_btn.click()
        return StackoverflowSignup()
