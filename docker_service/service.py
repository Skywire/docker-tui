from typing import List, Dict

from python_on_whales import DockerClient, Container
from python_on_whales.components.compose.models import ComposeConfigService
from textual import log


def get_docker_compose_services(compose_file: str) -> Dict[str, ComposeConfigService]:
    client = DockerClient(compose_files=[compose_file])
    compose_services = client.compose.config().services

    return compose_services

def get_containers() -> Dict[str, Container]:
    client = DockerClient()

    return {c.name: c for c in client.container.list(True)}
