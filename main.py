from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, TextLog

from docker_service.service import get_containers
from entities.project_db import get_projects
from screens.project_finder import ProjectFinder
from widgets.lov_viewer import LogViewer
from widgets.project_tree import ProjectTree


class DockerApp(App):
    BINDINGS = [
        ('q', 'quit', 'Quit'),
        ('a', 'push_screen("project_finder")', 'Add project'),
    ]

    SCREENS = {"project_finder": ProjectFinder()}

    TITLE = "Docker"

    DEFAULT_CSS = """
        #top-view {
            height: 80%;
        }
        #top-view ProjectTree {
            width: 20%;
        }
        #top-view LogViewer {
            width: 80%;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(ProjectTree(), LogViewer(), id='top-view')
        yield Horizontal(TextLog(id='docker-output', highlight=True))
        yield Footer()

    def on_mount(self) -> None:
        self.update_projects()

    def update_projects(self):
        projects = get_projects()

        tree = self.query_one(ProjectTree)
        tree.projects = projects

    def on_project_finder_project_added(self):
        self.pop_screen()
        self.update_projects()


if __name__ == '__main__':
    pass
