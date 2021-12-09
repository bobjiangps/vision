def test_non_ai_login_fail(web):
    """BVT-3: test login with wrong account using non ai elements"""
    web.log.info("user login")
    web.non_ai_link("xpath", "//a[contains(@href, 'login')]").click()
    web.non_ai_text_field("id", "username").input("test")
    web.non_ai_text_field("id", "password").input("111111")
    web.non_ai_button("xpath", "//input[@id='password']/following-sibling::button[@type='submit']").click()
    error_message = web.non_ai_static("xpath", "//p[@style='color:red']").wait_element_visible()
    web.log.info(error_message.text)
    assert error_message.text == "错误的用户名或密码"
