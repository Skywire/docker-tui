from __future__ import annotations

from datetime import timedelta

from python_on_whales import DockerClient
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.timer import Timer
from textual.widget import Widget
from textual.widgets import TextLog


class LogViewer(Container):
    text_log: TextLog
    container: str = reactive(None)
    docker: DockerClient
    update_timer: Timer = None

    def __init__(self, *children: Widget, name: str | None = None, id: str | None = None,
                 classes: str | None = None) -> None:
        super().__init__(*children, name=name, id=id, classes=classes)

        self.docker = DockerClient()

    def compose(self) -> ComposeResult:
        self.text_log = TextLog(highlight=True, markup=True)
        yield self.text_log

    def watch_container(self):
        self.start_logging()

    def start_logging(self) -> None:
        if not self.container:
            return

        if self.update_timer:
            self.update_timer.stop()
            self.text_log.clear()

        self.text_log.write(self.docker.logs(self.container))
        self.update_timer = self.set_interval(1, self.update_log, pause=False)

    def update_log(self):
        self.text_log.write(self.docker.logs(self.container, since=timedelta(milliseconds=1000)))
