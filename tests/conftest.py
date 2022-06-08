from lib.test_base.conftest import *
from lib.elements import ElementBase
from lib.non_ai_elements import NonAiElementBase
from lib.test_base.page_base import PageBase
from lib.visual.imager import Imager


@pytest.fixture(scope="function", autouse=True)
def web(logger):
    logger.info("Start web test.......")
    # web_test = type('web_test', (), {})()
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
    logger.info("Prepare resources in new machine only once.......")
    ElementBase.set_action(action)
    NonAiElementBase.set_action(action)
    Imager.activate_po()
    setattr(PageBase, "_driver", driver)
    setattr(PageBase, "action", action)
    setattr(PageBase, "log", logger)
    setattr(pytest, "web_test", PageBase)
    if home_page:
        action.browse_page(home_page)
    yield PageBase
    logger.info("Exit web test.......")
    SeleniumUtils.quit_driver()
