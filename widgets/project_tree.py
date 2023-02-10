import os
from typing import Optional, Dict

from python_on_whales import DockerClient, Service
from textual import events, log
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Tree, TreeNode

from config import config
from docker_service.service import get_containers
from entities.project_db import get_projects
from models.project_model import ProjectModel
from widgets.lov_viewer import LogViewer


class ProjectTree(Container):
    DEFAULT_CSS = """
    
        Tree {
            padding: 1 0 0 1;
        }
    """

    tree: Tree = None
    projects: Optional[Dict[str, ProjectModel]] = reactive(None)
    containers: Optional[Dict[str, Container]] = None
    selected_project: ProjectModel = None
    selected_service: Optional[Service] = None
    selected_node: TreeNode = None
    container_update_timer: Timer = None

    BINDINGS = [
        ('d', 'docker_down', 'Docker Down'),
        ('u', 'docker_up', 'Docker Up'),
        ('s', 'container_shell', 'Open Container Shell')
    ]

    def compose(self) -> ComposeResult:
        self.tree: Tree[dict] = Tree("Projects")
        self.tree.root.expand()
        self.containers = get_containers()
        self.text_log = self.app.query_one('#docker-output')

        yield self.tree

    def action_docker_up(self):
        docker: DockerClient = DockerClient(compose_files=self.selected_project.file)

        output = docker.compose.up(detach=True)

        for line in output:
            self.text_log.clear()
            self.text_log.write(line)

        self.containers = get_containers()
        self.set_projects(get_projects())

    def action_docker_down(self):
        docker: DockerClient = DockerClient(compose_files=self.selected_project.file)

        output = docker.compose.down()

        for line in output:
            self.text_log.clear()
            self.text_log.write(line)

        self.containers = get_containers()
        self.set_projects(get_projects())

    def action_container_shell(self):
        if not self.selected_service:
            return

        exec_cmd: str = str(config['docker_exec'])
        if not exec_cmd:
            return

        exec_cmd = exec_cmd.replace('{cmd}', f"-it {self.selected_service.container_name} bash")

        os.system(exec_cmd)

    def watch_projects(self, old, new) -> None:
        self.set_projects(new)

    def _on_mount(self, event: events.Mount) -> None:
        super()._on_mount(event)

        self.projects = get_projects()
        self.containers = get_containers()

        self.tree.focus()

        self.container_update_timer = self.set_interval(60, self.update_containers, pause=False)

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted):
        self.parent.query_one(LogViewer).container = None
        self.selected_service = None

        if not event.node.data or 'project' not in event.node.data.keys():
            return

        self.selected_project = event.node.data['project']
        if 'service' in event.node.data.keys():
            self.selected_service = event.node.data['service']

        if 'container' in event.node.data.keys():
            self.parent.query_one(LogViewer).container = event.node.data['container']

        self.selected_node = event.node

    def update_containers(self):
        self.containers = get_containers()
        self.set_projects(self.projects)

    def set_projects(self, projects):
        self.tree.clear()
        if self.projects:
            for project_name, project in projects.items():
                expand_project = False
                branch = self.tree.root.add(project_name, {"project": project})
                for service_name, service in project.services.items():
                    data = {"project": project, "service": service}

                    if service.container_name in self.containers.keys():
                        display_name = f"🟢 {service.container_name}"
                        data["container"] = self.containers[service.container_name]
                        expand_project = True
                    else:
                        display_name = f"🔴 {service.container_name}"

                    branch.add_leaf(display_name, data)

                if expand_project:
                    branch.expand()
        if self.selected_node:
            self.tree.get_node_by_id(self.selected_node.id).expand()
