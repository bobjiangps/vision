import pytest
import logging
import os
import datetime
from lib.visual.pred import *
from utils.selenium_utils import SeleniumUtils
from utils.yaml_helper import YamlHelper
from lib.action.web import WebAction
from py.xml import html
from pathlib import Path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    rep.description = str(item.function.__doc__)
    setattr(item, "rep_" + rep.when, rep)
    logger = logging.getLogger("System")
    if rep.when == "call":
        if rep.failed:
            logger.error(f"\x1b[0;31mScript [{item.function.__name__}] result is: Failed.\x1b[0m")
            logger.error(f"\x1b[0;31mFailure Details: {rep.longreprtext}\x1b[0m")
            driver = getattr(pytest, "web_test")._driver
            screenshot_file_path = Path.cwd().joinpath("results", "screenshots", "%s.png" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
            driver.save_screenshot(str(screenshot_file_path))
            extra_html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                   'onclick="window.open(this.src)" align="right"/></div>' % screenshot_file_path
            extra = getattr(rep, 'extra', [])
            extra.append(item.config.pluginmanager.getplugin('html').extras.html(extra_html))
            rep.extra = extra
        elif rep.passed:
            logger.info(f"\x1b[0;32mScript [{item.function.__name__}] result is: Pass.\x1b[0m")
        elif rep.skipped:
            logger.info(f"\x1b[0;33mScript [{item.function.__name__}] result is: Skipped.\x1b[0m")


def pytest_configure(config):
    logger = logging.getLogger("System")
    logger.info("loading model...")
    setattr(pytest, "model", init_model())
    # setattr(pytest, "model", init_model(name="state", remove=True, state=True))
    logger.info("model loaded...")
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


@pytest.fixture()
def logger():
    current_log = logging.getLogger(os.environ.get('PYTEST_CURRENT_TEST').split('::')[-2].split(' ')[0])
    return current_log


def pytest_html_results_table_header(cells):
    try:
        cells.insert(2, html.th('Description'))
        cells.insert(3, html.th('Time', class_='sortable time', col='time'))
        cells.pop()
    except Exception as e:
        print("error occur in header, cannot update report: %s" % str(e))


def pytest_html_results_table_row(report, cells):
    try:
        cells.insert(2, html.td(report.description))
        cells.insert(3, html.td(datetime.datetime.now(), class_='col-time'))
        cells.pop()
    except Exception as e:
        print("error occur in row, cannot update report: %s" % str(e))
