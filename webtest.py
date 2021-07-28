from prepare import Preparation


class WebTest(Preparation):
    def run(self):
        self.static("Login ID | Login name").input("test@test.com")
        self.button("Login | Sign in").click()
        input("press any key")


if __name__ == "__main__":
    old_url = ""
    new_url = ""

    wt = WebTest(old_url)
    with wt:
        wt.run()


# from models.pred import *
# from selenium import webdriver
# from lib.action.web import WebAction
# from selenium.webdriver.common.action_chains import ActionChains
#
#
# if __name__ == "__main__":
#     model = init_model()
#
#     old_url = ""
#     new_url = ""
#
#     driver = webdriver.Chrome()
#     driver.get(old_url)
#     wa = WebAction(driver, model)
#     c0 = wa.wait_until_text_display("Login ID | Login name")
#     login_btn = wa.wait_until_element_display("Button", "Login | Sign in")
#     offset, body = wa.check_offset()
#     ActionChains(driver).move_to_element_with_offset(body, c0[0], c0[1]+offset[1]).click().send_keys("test@test.com").perform()
#     ActionChains(driver).move_to_element_with_offset(body, login_btn[0], login_btn[1]+offset[1]).click().perform()
#     input("press any key")
#     driver.quit()


# from models.pred import *
# from selenium import webdriver
# from lib.action.web import WebAction
# from lib.elements.button import Button
# from lib.elements.static import Static
#
#
# if __name__ == "__main__":
#     model = init_model()
#
#     old_url = ""
#     new_url = ""
#
#     driver = webdriver.Chrome()
#     driver.get(new_url)
#     wa = WebAction(driver, model)
#     offset, body = wa.check_offset()
#     button = Button(driver, wa, offset)
#     static = Static(driver, wa, offset)
#     static("Login ID | Login name").input("test@test.com")
#     button("Login | Sign in").click()
#     input("press any key")
#     driver.quit()
