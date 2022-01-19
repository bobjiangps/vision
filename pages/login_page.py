from lib.test_base.page_base import PageBase


class LoginPage(PageBase):

    def __init__(self, platform):
        super().__init__(platform)
        self.login_static = platform.static("Login ID | Login name")
        self.password_field = platform.text_field("Password")
        self.login_btn = platform.button("Login | Sign in")
        self.account_option_static = platform.static("Account Options")

    def fill_account(self, account):
        self.platform.log.info("start to fill account")
        self.login_static.input(account)
        return self

    def fill_password(self, pw):
        self.platform.log.info("start to fill pw")
        self.password_field.input(pw)
        return self

    def click_login(self):
        self.platform.log.info("start to click login button")
        self.login_btn.click()
        return self

    def login_site(self, account, pw):
        self.platform.log.info("start to login")
        self.fill_account(account).fill_password(pw).click_login()
        self.login_btn.wait_element_disappear()
        self.account_option_static.wait_text_visible()

    def login_site_temp(self, account, pw):
        self.platform.log.info("start to login")
        self.platform.static("Login ID | Login name").input(account)
        self.platform.text_field("Password").input(pw)
        self.platform.button("Login | Sign in").click()
        self.platform.button("Login | Sign in").wait_element_disappear()
        self.platform.static("Account Options").wait_text_visible()
