from models.pred import *
from selenium import webdriver
from lib.action.web import WebAction
from selenium.webdriver.common.action_chains import ActionChains
import time

if __name__ == "__main__":
    model = init_model()

    old_url = ""
    new_url = ""

    driver = webdriver.Chrome()
    driver.get(old_url)
    wa = WebAction(driver, model)
    c0 = wa.wait_until_text_display("Login ID | Login name")
    print(c0)
    login_btn = wa.wait_until_element_display("Button", "Login | Sign in")
    print(login_btn)
    cart_btn = wa.wait_until_element_display("Button", "Cart")
    print(cart_btn)
    offset, body = wa.check_offset()
    print(offset)
    ActionChains(driver).move_to_element_with_offset(body, c0[0], c0[1]+offset[1]).click().send_keys("test@test.com").perform()
    time.sleep(3)
    ActionChains(driver).move_to_element_with_offset(body, login_btn[0], login_btn[1]+offset[1]).click().perform()
    input("press any key")
    driver.quit()
