from lib.test_base.page_base import PageBase


class NonAILoginPage(PageBase):

    def __init__(self, platform):
        super().__init__(platform)
        self.login_link = platform.non_ai_link("xpath", "//a[contains(@href, 'login')]")
        self.username_field = platform.non_ai_text_field("id", "username")
        self.password_field = platform.non_ai_text_field("id", "password")
        self.login_btn = platform.non_ai_button("xpath", "//input[@id='password']/following-sibling::button[@type='submit']")
        self.error_message = platform.non_ai_static("xpath", "//p[@style='color:red']")

    def fill_account(self, account):
        self.login_link.click()
        self.username_field.input(account)
        return self

    def fill_password(self, pw):
        self.password_field.input(pw)
        return self

    def click_login(self):
        self.login_btn.click()
        return self

    def login_failed_then_fetch_error_message(self, account, pw):
        self.platform.log.info("start to login")
        self.fill_account(account).fill_password(pw).click_login()
        return self.error_message.wait_element_visible().text
