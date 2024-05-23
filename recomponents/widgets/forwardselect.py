from enum import Enum
from typing import Iterable, Type

from textual import on
from textual.widgets import Select


class ForwardSelect[RenderableType, SelectType](Select):
    """
    A Select widget representing a one-way binding to an attribute of an object.
    """

    def __init__(self, item, attribute: str, options: Iterable[tuple[RenderableType, SelectType]], *args, **kwargs):
        self.item = item
        self.attribute = attribute
        if not hasattr(item, attribute):
            raise AttributeError(f"Item does not have attribute {attribute}")
        initial_value = getattr(item, attribute)
        super().__init__(options=options, value=initial_value, *args, **kwargs)

    @staticmethod
    def enum_options[T: Enum](enumeration: Type[T]) -> Iterable[tuple[str, T]]:
        """
        Create a list of ForwardSelect options from an Enum.
        """
        return [(member.name, member) for member in enumeration]

    @on(Select.Changed)
    def on_select_changed(self, event: Select.Changed) -> None:
        value = event.value
        if value == Select.BLANK:
            value = None
        setattr(self.item, self.attribute, value)
