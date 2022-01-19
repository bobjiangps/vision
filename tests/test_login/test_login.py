from pages.login_page import LoginPage


def test_cui_login_successful(web):
    """BVT-1: test login"""
    web.log.info("user login")
    web.static("Login ID | Login name").input("ANE54527")
    web.text_field("Password").input("123456")
    web.button("Login | Sign in").click()
    web.button("Login | Sign in").wait_element_disappear()
    web.static("Account Options").wait_text_visible()
    # # validate the restart attribute below
    # web.action.restart_browser()
    # web.action.browse_page("https://www.stackoverflow.com")
    # web.static("Log in").click()


def test_cui_login_fail(web):
    """BVT-2: test login with wrong account"""
    web.log.info("user login")
    web.static("Login ID | Login name").input("unknown")
    web.text_field("Password").input("123456")
    web.button("Login | Sign in").click()
    web.static("Invalid login name or password").wait_text_visible()


def test_cui_login_with_page_object(web):
    """BVT-3: test login with page object"""
    LoginPage(web).login_site("ANE54527", "123456")
    # LoginPage(web).fill_account("ANE54527").fill_password("123456").click_login()
