from typing import List, Dict

from textual import on
from textual.coordinate import Coordinate
from textual.message import Message
from textual.widgets import DataTable


class ObjectTable[T](DataTable):
    """
    DataTable, but more object-oriented.
    """

    class ObjectSelected[T](Message):
        """
        An event signifying that an object has been selected.
        """

        def __init__(self, item: T, trigger: DataTable.CellSelected):
            super().__init__()
            self.item: T = item
            self.trigger: DataTable.CellSelected = trigger

    def __init__(self, items: List[T],
                 fields: List[str] = None,
                 row_key_function=lambda item: str(id(item)),
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        if fields is None:
            if len(items) > 0:
                fields = list(vars(items[0]).keys())
            else:
                fields = []
        self.fields: List[str] = fields
        self.key_function = row_key_function
        self.items: Dict[str, T] = {self.key_function(item): item for item in items}

    def on_mount(self):
        for field in self.fields:
            self.add_column(field, key=str(field))
        for item in self.items.values():
            self.add_row(*[getattr(item, field) for field in self.fields], key=self.key_function(item))

    def coordinate_to_object(self, coord_row: int) -> T:
        (row_key, _) = self.coordinate_to_cell_key(Coordinate(coord_row, 0))
        return self.items[row_key.value]

    def refresh_object(self, item: T):
        """
        Refreshes the cells representing the given object.

        :param item:
        :return:
        """
        row_key = self.key_function(item)
        for field in self.fields:
            self.update_cell(row_key, field, getattr(item, field), update_width=True)

    def add_object(self, item: T):
        """
        Adds an object to the end of the table, if it is not already present.

        :param item:
        :return:
        """
        row_key = self.key_function(item)
        if row_key in self.items:
            return
        self.items[row_key] = item
        self.add_row(*[getattr(item, field) for field in self.fields], key=row_key)

    def move_to_object(self, item: T):
        row_key = self.key_function(item)
        row_index = self.get_row_index(row_key)
        self.move_cursor(row=row_index)
        # workaround for Textual-internal glitch where the cursor may be moved out of view
        self.call_after_refresh(self.move_cursor, row=row_index)

    @on(DataTable.CellSelected)
    def on_cell_selected(self, event: DataTable.CellSelected):
        """
        Handles native CellSelected event by posting a respective ObjectSelected event.

        :param event:
        :return:
        """
        row_key = event.cell_key.row_key
        object_at_row = self.items[row_key.value]
        self.post_message(
            ObjectTable.ObjectSelected(
                object_at_row,
                trigger=event
            )
        )

    def __contains__(self, *args, **kwargs):
        """
        Checks whether the table contains the given object.

        :param args:
        :param kwargs:
        :return:
        """
        row_key = self.key_function(args[0])
        return row_key in self.items
