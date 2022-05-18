from pages.stackoverflow_login import StackoverflowLogin


def test_show_error_message_if_input_nothing_when_login(web):
    """BVT-1: test show error message when login to stackoverflow"""
    web.log.info("go to login page")
    web.log.info("no xpath, no iframe, just define what you have seen")
    login_page = StackoverflowLogin()
    login_page.go_to_login_page_and_accept_cookie().login_without_input_anything()
    login_page.email_err_msg.wait_element_visible()
    login_page.password_err_msg.wait_element_visible()
    web.log.info("navigate to sign up page and input something")
    sign_up_page = login_page.navigate_to_signup_page()
    sign_up_page.only_input_in_text_fields()
