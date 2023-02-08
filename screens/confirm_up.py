from __future__ import annotations

from textual import events, log
from textual._types import MessageTarget as MessageTarget
from textual.app import ComposeResult
from textual.containers import Horizontal, Container
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label
from textual.widgets._header import HeaderIcon


class ConfirmUp(Screen):
    DEFAULT_CSS = """
        Screen {
            align: center middle;
        }
        Horizontal {
            align: center middle;
        }
        Label {
            width: 100%;
            content-align: center middle;
        }
        Button {
            margin: 1 1 1 1;
        }
        .box {
            width: 83;
            height: 9;
            margin: 1;
            padding: 1;
            background: green;
            color: white 90%;
            border: heavy white;
            align: center middle;
        }
    """

    class ConfirmResult(Message):

        def __init__(self, sender: MessageTarget, confirm: bool) -> None:
            self.confirm = confirm
            super().__init__(sender)

    def compose(self) -> ComposeResult:
        # yield Header()
        yield Container(
            Label("Other project containers are already running, continue with up?"),
            Horizontal(
                Button("Yes", id='confirm-yes'),
                Button("No", id='confirm-no'),
            ),
            classes='box'
        )
        # yield Footer()

    # def _on_mount(self, event: events.Mount) -> None:
    #     self.query_one(HeaderIcon).icon = '🐋';

    async def on_button_pressed(self, event: Button.Pressed):
        result = event.button.id == 'confirm-yes'
        self.app.pop_screen()
        # await self.emit(self.ConfirmResult(self, confirm=result))