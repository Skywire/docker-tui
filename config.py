import os
import shutil
from os.path import join

import yaml

config_path = join(os.path.expanduser('~'), '.docker-tui/config.yml')
config = {}


def load_config():
    if len(config):
        return

    if not os.path.isfile(config_path):
        template_path = os.path.dirname(os.path.realpath(__file__)) + '/.config.yml.dist'
        shutil.copy(template_path, config_path)

    with open(config_path, 'r') as file:
        for k, v in yaml.safe_load(file).items():
            config[k] = v


def get_project_home() -> str:
    if 'project_home' in config.keys() and config['project_home'] is not None:
        return config['project_home']

    return join(os.path.expanduser('~') + "/")


if __name__ == '__main__':
    load_config()
