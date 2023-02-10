from __future__ import annotations

import os
from os.path import join, dirname
from typing import Optional

from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import DirectoryTree, Button, Header, Footer, Label, ListView, ListItem, Checkbox
from textual.widgets._directory_tree import DirEntry
from textual.widgets._header import HeaderIcon

from config import get_project_home
from docker_service.service import find_compose_files, get_docker_compose_services
from entities.project_db import add_project
from models.project_model import ProjectModel


class ProjectScanner(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    DEFAULT_CSS = """
        .heading {
            content-align: center middle;
            padding: 1;
            width: 100%;
        }
        #content{
            width:80%;
        }
        DirectoryTree {
            height: 50%;
            padding: 1;
        }
        ListView {
            padding: 1;
        }
        #buttons {
            height:100%;
        }
        Button {
            margin: 0 1 0 1;
        }
        Checkbox {
            margin: 0;
            padding: 0;
        }
        Label {
            padding-top: 1;
        }
    """

    class ProjectAdded(Message):
        pass

    selected_dir: Optional[str] = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select a directory to recursively scan for docker-compose files", classes='heading')
        yield Horizontal(
            Vertical(
                DirectoryTree(get_project_home()),
                Label("Check a filename to add the project", classes='heading'),
                ListView(ListItem(Label("Waiting for scan")), id="file-list"),
                id="content"
            ),
            Vertical(
                Button("Scan", disabled=False, id="scan"),
                id="buttons"
            ),
        )
        yield Footer()

    def _on_mount(self, event: events.Mount) -> None:
        self.query_one(HeaderIcon).icon = '🐋';

    def on_tree_node_highlighted(self, event: DirectoryTree.NodeHighlighted):
        self.selected_dir = None

        if isinstance(event.node.data, DirEntry):
            self.selected_dir = event.node.data.path

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'scan':
            event.button.disabled = True

            file_list: ListView = self.query_one('#file-list')
            file_list.clear()

            exclude = ['\/vendor\/', '\/.github', '\/node_modules']
            for file in find_compose_files(self.selected_dir, exclude_patterns=exclude):
                file_list.append(
                    ListItem(Horizontal(Checkbox(False, name=file), Label(file)))
                )

            event.button.disabled = False

    async def on_checkbox_changed(self, event: Checkbox.Changed):
        if event.value:
            file = event.input.name
            project_name = dirname(file).split('/').pop()
            add_project(project_name, ProjectModel(
                name=project_name,
                file=file,
                services=get_docker_compose_services(file)))

            await self.emit(self.ProjectAdded(self))
