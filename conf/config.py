from lib.singleton import Singleton
from utils.yaml_helper import YamlHelper
from pathlib import Path
import argparse


class LoadConfig(Singleton):

    def __init__(self):
        self.data = YamlHelper.load_yaml(Path(__file__).absolute().parent.joinpath("config.yaml"))

    @property
    def model(self):
        return self.data["model"]

    @model.setter
    def model(self, dict_value):
        self.data["model"].update(dict_value)

    @property
    def command_parameter(self):
        return self.data["command_parameter"]

    @command_parameter.setter
    def command_parameter(self, dict_value):
        self.data["command_parameter"].update(dict_value)

    @staticmethod
    def set_command_parameter():
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", "--environment", metavar="QA", type=str, default="QA",
                            choices=["INT", "QA", "Staging", "PROD"],
                            help="a string that indicates which environment to test (INT, QA, Staging, PROD)")
        parser.add_argument("-b", "--browser", metavar="Chrome", type=str,
                            choices=["Safari", "Chrome", "Firefox", "Edge", "MobileBrowser"],
                            help="a string that indicates which browser to run web test")
        parser.add_argument("-t", "--test", metavar="test_class_name test_class_name.method_name", type=str, nargs="+",
                            help="a list of test classes or test methods which you want to run")
        parser.add_argument("-et", "--exclude_test", metavar="test_class_name test_class_name.method_name", type=str,
                            nargs="+", help="a list of test classes or test methods which not run")
        parser.add_argument("-T", "--tag", metavar="Happy_Path", type=str, default="All",
                            choices=["All", "Happy_Path", "Bad_Path", "Sad_Path"],
                            help="a string about the tag to define which cases to run")
        parser.add_argument("-k", "--keyword", metavar="", type=str,
                            help="a string about the keyword to define which cases to run, match case name")
        parser.add_argument("-m", "--marker", metavar="", type=str,
                            help="a string about the marker to define which cases to run, like categorization")
        parser.add_argument("-mp", "--mobile_platform", metavar="Android", type=str, choices=["Android", "iOS"],
                            help="a string that indicates which mobile system to run mobile app test")
        parser.add_argument("-d", "--device", metavar="Device", type=str,
                            help="a string that indicates which device to run mobile app test")
        parser.add_argument("-ll", "--log_level", metavar="DEBUG", type=str, default="DEBUG",
                            choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTEST"],
                            help="a string about log level to show log")
        return parser.parse_args().__dict__
