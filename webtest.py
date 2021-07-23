from models.pred import *
from selenium import webdriver
from pathlib import Path
from common.action.web import WebAction
from utils.image_processor import ImageProcessor as IP

if __name__ == "__main__":
    model = init_model()
    # results, labels = predict(model)
    # print(labels)
    # print(results)

    old_url = ""
    new_url = ""
    driver = webdriver.Chrome()
    print(driver.get_window_size())
    driver.get(old_url)
    wa = WebAction(driver, model)
    c1 = wa.wait_until_text_display("Login")
    print(c1)
    c2 = wa.wait_until_element_display("Button")
    print(c2)
    c3 = wa.wait_until_element_display("button", "Cart")
    print(c3)
    input("press any key")
    driver.quit()

