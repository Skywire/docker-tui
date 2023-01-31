from __future__ import annotations

import os
from os.path import join, dirname
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.screen import Screen
from textual.widgets import DirectoryTree, Button, TreeNode
from textual.widgets._directory_tree import DirEntry

from docker_service.service import get_docker_compose_services
from entities.project_db import add_project
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
    class ProjectAdded(Message):
        pass

    DEFAULT_CSS = """
        ProjectFinder DirectoryTree {
            width: 80%
        }
       ProjectFinder Button {
        } 
    """

    selected_file: str = None

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        name = "Add Project"
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        yield Horizontal(
            ComposeDirectoryTree(join(os.path.expanduser('~') + "/dev/magento")),
            Button("Add Project"))

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected):
        self.selected_file = event.path

    async def on_button_pressed(self, event: Button.Pressed):
        project_name = dirname(self.selected_file).split('/').pop()
        add_project(project_name, ProjectModel(
            name=project_name,
            file=self.selected_file,
            services=get_docker_compose_services(self.selected_file)))

        await self.emit(self.ProjectAdded(self))
