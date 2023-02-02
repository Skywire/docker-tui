import os
import shelve
from os.path import join

from models.project_model import ProjectModel

project_db_path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../var") + "/projects"
config_db_path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../var") + "/config"


def get_projects():
    projects = {}
    with shelve.open(project_db_path, 'c') as db:
        for k in db.keys():
            projects[k] = db.get(k)

    return projects


def add_project(name, project: ProjectModel) -> None:
    with shelve.open(project_db_path, 'c') as db:
        db[name] = project


def set_home_directory(path: str):
    with shelve.open(config_db_path, 'c') as db:
        db['home_directory'] = path


def get_home_directory() -> str:
    with shelve.open(config_db_path, 'c') as db:
        if 'home_directory' in db.keys():
            return str(db.get('home_directory'))

    return join(os.path.expanduser('~') + "/")


def has_home_directory() -> bool:
    with shelve.open(config_db_path, 'c') as db:
        return 'home_directory' in db.keys()

def delete_home_directory():
    with shelve.open(config_db_path, 'c') as db:
        del db['home_directory']

if __name__ == '__main__':
    print(get_projects())
