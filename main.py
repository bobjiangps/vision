import pytest
import sys
import datetime
from conf.config import LoadConfig
from pathlib import Path


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        command_data = LoadConfig().command_parameter
    else:
        command_data = LoadConfig().set_command_parameter()
    setattr(pytest, "command_data", command_data)
    Path.cwd().joinpath("results", "reports").mkdir(exist_ok=True, parents=True)
    Path.cwd().joinpath("results", "logs").mkdir(exist_ok=True, parents=True)
    Path.cwd().joinpath("results", "screenshots").mkdir(exist_ok=True, parents=True)
    report_suffix = None
    if command_data["browser"]:
        report_suffix = command_data["browser"]
    elif command_data["mobile_platform"]:
        report_suffix = f"{command_data['mobile_platform']}_{command_data['device']}"
    if report_suffix:
        report_path = Path.cwd().joinpath("results", "reports", "AutoTest-%s-%s-%s.html"
                                          % (command_data["environment"], datetime.datetime.now().strftime("%Y%m%d%H%M%S"), report_suffix))
        command_list = ["--html", str(report_path)]
        if command_data["test"]:
            for in_test in command_data["test"].split(","):
                command_list.append(str(Path.cwd().joinpath("tests", in_test.strip())))
        elif not command_data["test"]:
            command_list.append(str(Path.cwd().joinpath("tests")))
        elif command_data["exclude_test"]:
            for ex_test in command_data["exclude_test"].split(","):
                command_list.extend(("--deselect", str(Path.cwd().joinpath("tests", ex_test.strip()))))
        if command_data["keyword"]:
            command_list.extend(("-k", command_data["keyword"].strip()))
        if command_data["marker"]:
            command_list.extend(("-m", command_data["marker"].strip()))
        command_list.extend(("--log-file", str(Path.cwd().joinpath("results", "logs", "AutoTest-%s.log" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")))))
        pytest.main(command_list)
    else:
        raise Exception("Error! Check running parameter!")
