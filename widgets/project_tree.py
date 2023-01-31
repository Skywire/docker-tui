from typing import Optional, Dict

from textual import events, log
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Tree

from models.project_model import ProjectModel
from widgets.lov_viewer import LogViewer


class ProjectTree(Container):
    tree: Tree = None
    projects: Optional[Dict[str, ProjectModel]] = reactive(None)
    containers: Optional[Dict[str, Container]] = reactive(None)

    def compose(self) -> ComposeResult:
        log("compose")
        self.tree: Tree[dict] = Tree("Projects")
        self.tree.root.expand()

        yield self.tree

    def watch_projects(self, old, new) -> None:
        self.set_projects(new)

    def _on_mount(self, event: events.Mount) -> None:
        super()._on_mount(event)

        self.tree.focus()

    def on_tree_node_selected(self, event: Tree.NodeSelected):
        log(event.node.data)
        if 'container' in event.node.data.keys():
            self.parent.query_one(LogViewer).container = event.node.data['container']

    def set_projects(self, projects):
        self.tree.clear()
        if self.projects:
            for project_name, project in projects.items():
                branch = self.tree.root.add(project_name, {"project": project_name})
                for service_name, service in project.services.items():
                    data = {"project": project, "service": service}

                    if service.container_name in self.containers.keys():
                        display_name = f"🟢 {service.container_name}"
                        data["container"] = self.containers[service.container_name]
                    else:
                        display_name = f"🔴 {service.container_name}"
                    branch.add_leaf(display_name, data)
