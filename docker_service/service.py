import os
import re
from typing import List, Dict, Generator, Optional

from python_on_whales import DockerClient, Container
from python_on_whales.components.compose.models import ComposeConfigService


def get_docker_compose_services(compose_file: str) -> Dict[str, ComposeConfigService]:
    client = DockerClient(compose_files=[compose_file])
    compose_services = client.compose.config().services

    return compose_services


def get_containers() -> Dict[str, Container]:
    client = DockerClient()

    return {c.name: c for c in client.container.list(True)}


def find_compose_files(start_path: str, exclude_patterns: Optional[List[str]] = None) -> Generator[str, None, None]:
    def is_excluded(path) -> bool:
        if not exclude_patterns:
            return False

        for pattern in exclude_patterns:
            if re.search(pattern, path):
                return True
        return False

    for root, dirs, files in os.walk(start_path):
        for name in files:
            if 'docker-compose' in name and not is_excluded(root):
                yield os.path.join(root, name)
