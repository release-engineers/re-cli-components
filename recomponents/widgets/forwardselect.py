from typing import Iterable

from textual import on
from textual.widgets import Select


class ForwardSelect[RenderableType, SelectType](Select):
    """
    A Select widget representing a one-way binding to an attribute of an object.
    """

    def __init__(self, item, attribute: str, values: Iterable[tuple[RenderableType, SelectType]], *args, **kwargs):
        self.item = item
        self.attribute = attribute
        if not hasattr(item, attribute):
            raise AttributeError(f"Item does not have attribute {attribute}")
        initial_value = getattr(item, attribute)
        super().__init__(options=values, value=initial_value, *args, **kwargs)

    @on(Select.Changed)
    def on_select_changed(self, event: Select.Changed) -> None:
        value = event.value
        if value == Select.BLANK:
            value = None
        setattr(self.item, self.attribute, value)
