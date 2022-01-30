from lib.test_base.page_base import *


class LoginPage(PageBase):

    def __init__(self):
        self.login_static = Static("Login ID | Login name")
        self.password_field = TextField("Password")
        self.login_btn = Button("Login | Sign in")
        self.account_option_static = Static("Account Options")

    def fill_account(self, account):
        self.login_static.input(account)
        return self

    def fill_password(self, pw):
        self.password_field.input(pw)
        return self

    def click_login(self):
        self.login_btn.click()
        return self

    def login_site(self, account, pw):
        self.log.info("start to login")
        self.fill_account(account).fill_password(pw).click_login()
        self.login_btn.wait_element_disappear()
        self.account_option_static.wait_text_visible()
        # here can return another page object like Home()
