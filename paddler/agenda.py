"""
High level classes that handle the task list, i.e. the scrollable pane at the
top of the main screen, above the console.
"""

from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Generic

# Type that describes low-level widget classes
WidgetT = TypeVar('WidgetT')


# TODO: how to handle keybindings?
#
# Idea #1: for now set them up in the tui/__init__.py as sensible
# defaults. We don't have to outsource them, they're part of the low-level TUI
# widget classes anyway. E.g. TUIInputField doesn't set the <return>
# keybinding, it uses prompt_toolkit.widget.TextArea's default - there's no
# reason why other widgets shouldn't do the same. If it ever becomes an issue,
# at least all of them will be in one place.
#
# Note to self: if there ever arises a need for a keybindings configuration,
# the KeyBindings class from prompt toolkit must be wrapped into a higher-level
# facade class anyway.
#
# Idea #2: Set keybindings in the inits of the control classes. Make the
# bound callbacks call control classes fields. Make the high-level classes
# substitute these callbacks with their versions.

class TaskCard(Generic[WidgetT], metaclass=ABCMeta):
    """Abstract base for an expandable container with task details."""
    widget: WidgetT

    @abstractmethod
    def toggle(self) -> None:
        """Expand or shrink the card."""

    @abstractmethod
    @property
    def collapsed(self) -> None:
        """Return True if the card is collapsed, False otherwise."""


class AgendaPane(Generic[WidgetT], metaclass=ABCMeta):
    """Abstract base for a pane with list of tasks."""

    @abstractmethod
    def add_card(self, card_widget: WidgetT):
        """Add / show the task card in the pane."""

    @abstractmethod
    def remove_card(self, card_idx: int) -> None:
        """Remove / hide the task card from the pande."""

    @abstractmethod
    def focus_on(self, card_idx: int) -> None:
        """Switch focus to a card under given index."""

    @abstractmethod
    @property
    def currently_focused(self) -> int:
        """Return the index of the currently focused task card."""


class Task:
    """Manages information visible on a task card."""
    def __init__(self, task_card: TaskCard):
        self.card = task_card


class Agenda:
    """Manages displaying tasks"""
    def __init__(self, agenda_pane: AgendaPane):
        self._pane = agenda_pane
        self._tasks: List[Task] = []

    def add_task(self, task: Task):
        pass

    def remove_task(self, task_idx: int):
        pass

    def _toggle_task_handler(self, focused_task_idx: int):
        pass

    def _remove_task_handler(self, focused_task_idx: int):
        pass
