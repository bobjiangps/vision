import yaml


class YamlHelper:

    @classmethod
    def load_yaml(cls, file_path):
        with open(file_path, "r") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        return data

    @classmethod
    def dump_yaml(cls, file_path, data):
        with open(file_path, "w") as f:
            yaml.dump(data, f)
