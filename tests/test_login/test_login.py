def test_cui_login_successful(web):
    """BVT-1: test login"""
    web.log.info("user login")
    web.static("Login ID | Login name").input("ANE54527")
    web.text_field("Password").input("123456")
    web.button("Login | Sign in").click()
    web.button("Login | Sign in").wait_element_disappear()
    web.static("Account Options").wait_text_visible()
    # validate the restart attribute below
    web.action.restart_browser()
    web.action.browse_page("https://www.stackoverflow.com")
    web.static("Log in").click()


def test_cui_login_fail(web):
    """BVT-2: test login with wrong account"""
    web.log.info("user login")
    web.static("Login ID | Login name").input("unknown")
    web.text_field("Password").input("123456")
    web.button("Login | Sign in").click()
    web.static("Invalid login name or password").wait_text_visible()
