import os
import shelve
from os.path import join

from models.project_model import ProjectModel

db_root = join(os.path.expanduser('~'), '.docker-tui')
os.makedirs(db_root, exist_ok=True)
project_db_path = db_root + "/projects"


def get_projects():
    projects = {}
    with shelve.open(project_db_path, 'c') as db:
        for k in db.keys():
            projects[k] = db.get(k)

    return projects


def add_project(name, project: ProjectModel) -> None:
    with shelve.open(project_db_path, 'c') as db:
        db[name] = project


if __name__ == '__main__':
    print(get_projects())
