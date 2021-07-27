from lib.singleton import Singleton
from utils.yaml_helper import YamlHelper
from pathlib import Path


class LoadConfig(Singleton):

    def __init__(self):
        self.data = YamlHelper.load_yaml(Path(__file__).absolute().parent.joinpath("config.yaml"))

    @property
    def model(self):
        return self.data["model"]

    @model.setter
    def model(self, dict_value):
        self.data["model"].update(dict_value)
