from __future__ import annotations

from os.path import dirname
from pathlib import Path
from typing import Optional

from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import DirectoryTree, Button, TreeNode, Header, Footer, Label
from textual.widgets._directory_tree import DirEntry
from textual.widgets._header import HeaderIcon

from docker_service.service import get_docker_compose_services
from entities.project_db import add_project, get_home_directory, set_home_directory, has_home_directory, \
    delete_home_directory
from models.project_model import ProjectModel


class ComposeDirectoryTree(DirectoryTree):

    def load_directory(self, node: TreeNode[DirEntry]) -> None:
        assert node.data is not None
        dir_path = Path(node.data.path)
        node.data.loaded = True
        directory = sorted(
            list(dir_path.iterdir()),
            key=lambda path: (not path.is_dir(), path.name.lower()),
        )
        for path in directory:
            if path.is_dir() or "docker-compose" in path.name:
                node.add(
                    path.name,
                    data=DirEntry(str(path), path.is_dir()),
                    allow_expand=path.is_dir(),
                )
        node.expand()


class ProjectFinder(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    DEFAULT_CSS = """
        #heading {
            content-align: center middle;
            padding: 1;
            width: 100%;
        }
        ProjectFinder DirectoryTree {
            width: 80%;
        }
        ProjectFinder Button {
            margin: 0 1 0 1;
        }
    """

    class ProjectAdded(Message):
        pass

    selected_file: Optional[str] = None
    selected_dir: Optional[str] = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select a docker-compose file to add", id='heading')
        yield Horizontal(
            ComposeDirectoryTree(get_home_directory()),
            Vertical(
                Button("Add Project", disabled=True, id="add"),
                Button("Set home directory", disabled=True,
                       id="home"),
                Button("Unset home directory", disabled=not has_home_directory(),
                       id="unset_home"),
                id="buttons"
            ),
        )
        yield Footer()

    def _on_mount(self, event: events.Mount) -> None:
        self.query_one(HeaderIcon).icon = '🐋';

    def on_tree_node_highlighted(self, event: DirectoryTree.NodeHighlighted):
        self.selected_file = None
        self.selected_dir = None
        self.query_one('#add').disabled = True
        self.query_one('#home').disabled = True

        if isinstance(event.node.data, DirEntry):
            self.query_one('#home').disabled = False
            self.selected_dir = event.node.data.path

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        self.query_one('#add').disabled = False
        self.selected_file = event.path

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'add':
            project_name = dirname(self.selected_file).split('/').pop()
            add_project(project_name, ProjectModel(
                name=project_name,
                file=self.selected_file,
                services=get_docker_compose_services(self.selected_file)))

            await self.emit(self.ProjectAdded(self))

        if event.button.id == "unset_home" and has_home_directory():
            delete_home_directory()
            self.query_one('#unset_home').disabled = True

        if event.button.id == "home":
            set_home_directory(self.selected_dir)
            self.query_one('#unset_home').disabled = False

        self.query_one(ComposeDirectoryTree).remove()
        await self.mount(ComposeDirectoryTree(get_home_directory()), before=self.query_one('#buttons'))
