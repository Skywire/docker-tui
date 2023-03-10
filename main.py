import sys
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from typing import Iterator

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, TextLog
from textual.widgets._header import HeaderIcon

from config import load_config
from entities.project_db import get_projects
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
        load_config()
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

    @contextmanager
    def suspend(self) -> Iterator[None]:
        driver = self.app._driver

        if driver is not None:
            driver.stop_application_mode()
            with redirect_stdout(sys.__stdout__), redirect_stderr(sys.__stderr__):
                yield
            driver.start_application_mode()

if __name__ == '__main__':
    load_config()

    app = DockerApp()
    app.run()
