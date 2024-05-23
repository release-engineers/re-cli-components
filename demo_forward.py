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
        self.my_field_1 = my_field
        self.my_field_2 = my_field
        self.my_field_3 = my_field


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.item = Item(ItemFieldEnum.BOB)

    def compose(self) -> ComposeResult:
        yield ForwardSelect(self.item, "my_field_1", ForwardSelect.enum_options(ItemFieldEnum))
        yield ForwardSelect(self.item, "my_field_2", ForwardSelect.enum_options(ItemFieldEnum))
        yield ForwardSelect(self.item, "my_field_3", ForwardSelect.enum_options(ItemFieldEnum))
        yield Label()

    @on(Select.Changed)
    def refresh_label(self):
        label = self.query_one(Label)
        label.update(f"Selected: {self.item.my_field_1}, {self.item.my_field_2}, {self.item.my_field_3}")


if __name__ == "__main__":
    app = MainApp()
    app.run()
