#!/usr/bin/env python
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Label, Select

from recomponents.widgets.forwardselect import ForwardSelect


class Item:
    def __init__(self, my_field: str):
        self.my_field = my_field


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.forward_select = ForwardSelect(Item("b"), "my_field", [("The A", "a"), ("The B", "b")])

    def compose(self) -> ComposeResult:
        yield self.forward_select
        yield Label()
        self.set_interval(1, self.refresh_label)

    @on(Select.Changed)
    def refresh_label(self):
        label = self.query_one(Label)
        label.update(f"Selected: {self.forward_select.item.my_field}")
        label.refresh()


if __name__ == "__main__":
    app = MainApp()
    app.run()
