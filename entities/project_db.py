import shelve
import os

from models.project_model import ProjectModel

db_path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../var") + "/projects"

def get_projects():
    projects = {}
    with shelve.open(db_path, 'c') as db:
        for k in db.keys():
            projects[k] = db.get(k)

    return projects

def add_project(name, project: ProjectModel) -> None:
    with shelve.open(db_path, 'c') as db:
        db[name] = project

if __name__ == '__main__':
    print(get_projects())
