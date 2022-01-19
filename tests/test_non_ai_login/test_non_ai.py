from pages.non_ai_login_page import NonAILoginPage


def test_non_ai_login_fail(web):
    """BVT-4: test login with wrong account using non ai elements"""
    web.log.info("user login")
    web.non_ai_link("xpath", "//a[contains(@href, 'login')]").click()
    web.non_ai_text_field("id", "username").input("test")
    web.non_ai_text_field("id", "password").input("111111")
    web.non_ai_button("xpath", "//input[@id='password']/following-sibling::button[@type='submit']").click()
    error_message = web.non_ai_static("xpath", "//p[@style='color:red']").wait_element_visible()
    web.log.info(error_message.text)
    assert error_message.text == "错误的用户名或密码"


def test_non_ai_login_fail_with_page_object(web):
    """BVT-5: test login with wrong account using non ai elements with page object"""
    error_message = NonAILoginPage(web).login_failed_then_fetch_error_message("test", "111111")
    web.log.info(error_message)
    assert error_message == "错误的用户名或密码"
