def test_cui_login(web):
    web.static("Login ID | Login name").input("ANE54527")
    web.text_field("Password").input("123456")
    web.button("Login | Sign in").click()
