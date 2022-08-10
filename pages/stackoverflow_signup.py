from lib.test_base.page_base import *


class StackoverflowSignup(PageBase):

    def __init__(self):
        super().__init__()
        self.name_field = TextField("Display name")
        self.email_field = TextField("Email")
        self.password_field = TextField("Password")

    def only_input_in_text_fields(self):
        self.name_field.input("bob")
        self.email_field.input("test@null.com")
        self.password_field.input(123456)
        return self

