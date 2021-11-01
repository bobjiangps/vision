import pytest
import logging
import os
from models.pred import *
from utils.selenium_utils import SeleniumUtils
from lib.action.web import WebAction


def pytest_configure(config):
    print("loading model...")
    setattr(pytest, "model", init_model())
    print("model loaded...")
    command_data = getattr(pytest, "command_data")
    if hasattr(config, '_metadata'):
        for item in ["Packages", "Plugins", "JAVA_HOME"]:
            if item in config._metadata.keys():
                del config._metadata[item]
        config._metadata["Environment"] = command_data["environment"]
        if command_data["browser"]:
            config._metadata["Browser"] = command_data["browser"]
        elif command_data["mobile_platform"]:
            config._metadata["Mobile Platform"] = command_data["mobile_platform"]
            config._metadata["Device"] = command_data["device"]


# not use pytest_addoption, because it does not allow lower case parameter
# def pytest_addoption(parser):
#     parser.addoption("-E", action="store", required=False, default="QA", help="which environment to test")
#     parser.addoption("-B", action="store", required=False, default="Chrome", help="which browser to test")


@pytest.fixture(scope="function")
def web(logger):
    logger.info("Start web test.......")
    web_test = type('web_test', (), {})()
    command_data = getattr(pytest, "command_data")
    url = ""
    driver = SeleniumUtils.get_driver(command_data["browser"])
    action = WebAction(driver, getattr(pytest, "model"))
    setattr(web_test, "_driver", driver)
    setattr(web_test, "action", action)
    setattr(web_test, "log", logger)
    setattr(pytest, "web_test", web_test)
    action.browse_page(url)
    yield web_test
    logger.info("Exit web test.......")
    SeleniumUtils.quit_driver()


@pytest.fixture()
def logger():
    current_log = logging.getLogger(os.environ.get('PYTEST_CURRENT_TEST').split('::')[-2].split(' ')[0])
    return current_log
