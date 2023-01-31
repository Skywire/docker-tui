from typing import List, Optional, Dict

from pydantic import BaseModel
from python_on_whales.components.compose.models import ComposeConfigService


class ProjectModel(BaseModel):
    name: str
    file: str
    services: Optional[Dict[str, ComposeConfigService]]

