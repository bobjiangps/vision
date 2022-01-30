from pages.login_page import LoginPage
from lib.elements import *


def test_cui_login_successful(web):
    """BVT-1: test login"""
    web.log.info("user login")
    Static("Login ID | Login name").input("ANE54527")
    TextField("Password").input("123456")
    Button("Login | Sign in").click()
    Button("Login | Sign in").wait_element_disappear(5)
    Static("Account Options").wait_text_visible(10)
    # # validate the restart attribute below
    web.restart_browser()
    web.browse_page("https://www.stackoverflow.com")
    Static("Log in").click()


def test_cui_login_fail(web):
    """BVT-2: test login with wrong account"""
    web.log.info("user login")
    Static("Login ID | Login name").input("unknown")
    TextField("Password").input("123456")
    Button("Login | Sign in").click()
    Static("Invalid login name or password").wait_text_visible()


def test_cui_login_with_page_object():
    """BVT-3: test login with page object"""
    # LoginPage().login_site("ANE54527", "123456")
    # LoginPage().fill_account("ANE54527").fill_password("123456").click_login()
    login_page = LoginPage()
    login_page.login_site("ANE54527", "123456")
    login_page.login_btn.wait_element_disappear()
