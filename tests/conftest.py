from lib.test_base.conftest import *


@pytest.fixture(scope="function")
def web(logger):
    logger.info("Start web test.......")
    web_test = type('web_test', (), {})()
    command_data = getattr(pytest, "command_data")
    url_file = Path.cwd().joinpath("data", "url.yaml")
    home_page = None
    if Path.exists(url_file):
        url_data = YamlHelper.load_yaml(url_file)
        try:
            home_page = url_data["web"]["home_page"][command_data["environment"]]
        except (KeyError, AttributeError):
            pass
    driver = SeleniumUtils.get_driver(command_data["browser"])
    action = WebAction(driver, getattr(pytest, "model"), logger)
    setattr(web_test, "_driver", driver)
    setattr(web_test, "action", action)
    setattr(web_test, "log", logger)
    setattr(pytest, "web_test", web_test)
    if home_page:
        action.browse_page(home_page)
    yield web_test
    logger.info("Exit web test.......")
    SeleniumUtils.quit_driver()
