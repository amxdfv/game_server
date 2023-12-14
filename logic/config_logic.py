import yaml


def read_config():
    with open('config.yaml') as config_yaml:
        config_data = yaml.load(config_yaml, Loader=yaml.FullLoader)
    return config_data
