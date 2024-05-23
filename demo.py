#!/usr/bin/env python
from textual import on
from textual.app import App, ComposeResult

from recomponents.widgets.objecttable import ObjectTable


class Item:
    def __init__(self, a: str, b: str):
        self.a = a
        self.b = b


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.table = ObjectTable[Item]([], fields=["a", "b"])

    def compose(self) -> ComposeResult:
        yield self.table

    def on_mount(self):
        items = [
            Item("a", "b"),
            Item("c", "d"),
            Item("e", "f"),
        ]
        for item in items:
            self.table.add_object(item)
        items[1].a = "x"
        self.table.refresh_object(items[1])
        self.table.move_to_object(items[1])
        self.table.action_select_cursor()

    @on(ObjectTable.ObjectSelected)
    def on_object_selected(self, event: ObjectTable.ObjectSelected[Item]):
        event.item.b = "this row was selected"
        self.table.refresh_object(event.item)


if __name__ == "__main__":
    app = MainApp()
    app.run()
