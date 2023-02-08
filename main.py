from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, TextLog
from textual.widgets._header import HeaderIcon

from entities.project_db import get_projects
from screens.confirm_up import ConfirmUp
from screens.project_finder import ProjectFinder
from screens.project_scanner import ProjectScanner
from widgets.lov_viewer import LogViewer
from widgets.project_tree import ProjectTree


class DockerApp(App):
    BINDINGS = [
        ('q', 'quit', 'Quit'),
        ('a', 'push_screen("project_finder")', 'Add project'),
    ]

    SCREENS = {
        "project_finder": ProjectFinder(),
        "project_scanner": ProjectScanner()

    }

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
        self.query_one(HeaderIcon).icon = '🐋'

    def update_projects(self):
        projects = get_projects()

        tree = self.query_one(ProjectTree)
        tree.projects = projects

    def on_project_finder_project_added(self):
        self.pop_screen()
        self.update_projects()

    def on_project_scanner_project_added(self):
        self.update_projects()

    async def on_confirm_up_confirm_result(self, event: ConfirmUp.ConfirmResult):
        self.pop_screen()

        if event.confirm:
            tree: ProjectTree = self.query_one(ProjectTree)
            tree.docker_up()


if __name__ == '__main__':
    app = DockerApp()
    app.run()
