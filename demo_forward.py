#!/usr/bin/env python
from enum import Enum

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Label, Select

from recomponents.widgets.forwardselect import ForwardSelect


class ItemFieldEnum(Enum):
    ALICE = "a"
    BOB = "b"


class Item:
    def __init__(self, my_field: ItemFieldEnum):
        self.my_field = my_field


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.forward_select = ForwardSelect(Item(ItemFieldEnum.BOB), "my_field", ForwardSelect.enum_options(ItemFieldEnum))

    def compose(self) -> ComposeResult:
        yield self.forward_select
        yield Label()

    @on(Select.Changed)
    def refresh_label(self):
        label = self.query_one(Label)
        label.update(f"Selected: {self.forward_select.item.my_field}")


if __name__ == "__main__":
    app = MainApp()
    app.run()
