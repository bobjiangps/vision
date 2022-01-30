from pages.non_ai_login_page import NonAILoginPage
from lib.non_ai_elements import *


def test_non_ai_login_fail(web):
    """BVT-4: test login with wrong account using non ai elements"""
    web.log.info("user login")
    NonAiLink("xpath", "//a[contains(@href, 'login')]").click()
    NonAiTextField("id", "username").input("test")
    NonAiTextField("id", "password").input("111111")
    NonAiButton("xpath", "//input[@id='password']/following-sibling::button[@type='submit']").click()
    error_message = NonAiStatic("xpath", "//p[@style='color:red']").wait_element_visible()
    web.log.info(error_message.text)
    assert error_message.text == "错误的用户名或密码"


def test_non_ai_login_fail_with_page_object(web):
    """BVT-5: test login with wrong account using non ai elements with page object"""
    error_message = NonAILoginPage().login_failed_then_fetch_error_message("test", "111111")
    web.log.info(error_message)
    assert error_message == "错误的用户名或密码"
