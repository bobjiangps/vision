from models.pred import *
from selenium import webdriver
from common.action.web import WebAction
from selenium.webdriver.common.action_chains import ActionChains
import time

if __name__ == "__main__":
    model = init_model()

    old_url = ""
    new_url = ""

    driver = webdriver.Chrome()
    driver.get(old_url)
    wa = WebAction(driver, model)
    c0 = wa.wait_until_text_display("Login")
    print(c0)
    login_btn = wa.wait_until_element_display("Button")
    print(login_btn)
    body = driver.find_element_by_xpath("//html//body")
    ActionChains(driver).move_to_element_with_offset(body, c0[0], c0[1]).click().send_keys("test@test.com").perform()
    time.sleep(3)
    ActionChains(driver).move_to_element_with_offset(body, login_btn[0], login_btn[1]).click().perform()
    input("press any key")
    driver.quit()

