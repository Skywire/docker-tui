from typing import Optional, Dict

from python_on_whales import DockerClient
from textual import events, log
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Tree

from docker_service.service import get_containers
from entities.project_db import get_projects
from models.project_model import ProjectModel
from widgets.lov_viewer import LogViewer


class ProjectTree(Container):
    tree: Tree = None
    projects: Optional[Dict[str, ProjectModel]] = reactive(None)
    containers: Optional[Dict[str, Container]] = None
    selected_project: ProjectModel = None

    BINDINGS = [
        ('d', 'docker_down', 'Docker Down'),
        ('u', 'docker_up', 'Docker Up')
    ]

    def compose(self) -> ComposeResult:
        self.tree: Tree[dict] = Tree("Projects")
        self.tree.root.expand()
        self.containers = get_containers()

        yield self.tree

    def action_docker_up(self):
        docker: DockerClient = DockerClient(compose_files=self.selected_project.file)

        docker.compose.up(detach=True)

        self.containers = get_containers()
        self.set_projects(get_projects())

    def action_docker_down(self):
        docker: DockerClient = DockerClient(compose_files=self.selected_project.file)

        docker.compose.down()

        self.containers = get_containers()
        self.set_projects(get_projects())

    def watch_projects(self, old, new) -> None:
        self.set_projects(new)

    def _on_mount(self, event: events.Mount) -> None:
        super()._on_mount(event)

        self.projects = get_projects()
        self.containers = get_containers()

        self.tree.focus()

    def on_tree_node_selected(self, event: Tree.NodeSelected):
        if 'container' in event.node.data.keys():
            self.parent.query_one(LogViewer).container = event.node.data['container']

        self.selected_project = event.node.data['project']

    def set_projects(self, projects):
        self.tree.clear()
        if self.projects:
            for project_name, project in projects.items():
                branch = self.tree.root.add(project_name, {"project": project})
                for service_name, service in project.services.items():
                    data = {"project": project, "service": service}

                    if service.container_name in self.containers.keys():
                        display_name = f"🟢 {service.container_name}"
                        data["container"] = self.containers[service.container_name]
                    else:
                        display_name = f"🔴 {service.container_name}"

                    branch.add_leaf(display_name, data)
