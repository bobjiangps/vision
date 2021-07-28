from models.pred import *
from selenium import webdriver
from lib.action.web import WebAction
from lib.elements.button import Button
from lib.elements.static import Static


class Preparation:

    def __init__(self, url):
        self.url = url

    def __enter__(self):
        self.model = init_model()
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.wa = WebAction(self.driver, self.model)
        self.offset, _ = self.wa.check_offset()
        self.button = Button(self.driver, self.wa, self.offset)
        self.static = Static(self.driver, self.wa, self.offset)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
