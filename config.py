import os
from os.path import join

import yaml

config_path = join(os.path.expanduser('~'), '.docker-tui/config.yml')
config = {}


def load_config():
    if len(config):
        return

    if not os.path.isfile(config_path):
        with open(config_path, 'w') as file:
            file.writelines(get_default_config())

    with open(config_path, 'r') as file:
        for k, v in yaml.safe_load(file).items():
            config[k] = v


def get_project_home() -> str:
    if 'project_home' in config.keys() and config['project_home'] is not None:
        return config['project_home']

    return join(os.path.expanduser('~') + "/")


def get_default_config():
    return f"""project_home: {get_project_home()}""" + \
        """
# docker_exec: gnome-terminal -- docker exec {cmd} # linux
# docker_exec: osascript -e 'tell app "Terminal" to do script "docker exec {cmd}"' # macOS
"""


if __name__ == '__main__':
    load_config()
