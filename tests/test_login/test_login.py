def test_cui_login(web):
    web.static("Login ID | Login name").input("ANE54527")
    web.text_field("Password").input("123456")
    web.button("Login | Sign in").click()
    # validate the restart attribute below
    import time
    time.sleep(5)
    web.action.restart_browser()
    web.action.browse_page("https://www.stackoverflow.com")
    web.static("Log in").click()
    time.sleep(5)
