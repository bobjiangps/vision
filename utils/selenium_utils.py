from selenium import webdriver


class SeleniumUtils:
    _driver = None
    _name = None

    @classmethod
    def get_driver(cls, name):
        cls._name = name
        if cls._driver is None:
            cls._driver = globals()[name].create()
        return cls._driver

    @classmethod
    def close_browser(cls):
        if cls._driver is not None:
            cls._driver.close()

    @classmethod
    def quit_driver(cls):
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None

    @classmethod
    def restart_driver(cls, name=None):
        cls.quit_driver()
        if name is None:
            cls.get_driver(cls._name)
        else:
            cls.get_driver(name)
        return cls._driver


class Chrome:

    @classmethod
    def create(cls):
        return webdriver.Chrome()


class Firefox:

    @classmethod
    def create(cls):
        return webdriver.Firefox()


class Edge:

    @classmethod
    def create(cls):
        return webdriver.Edge()


class Safari:

    @classmethod
    def create(cls):
        return webdriver.Safari()
