"""
High level classes that handle the console window, i.e. the text areas at the
bottom of the screen.
"""

from abc import ABCMeta, abstractmethod
from queue import Queue

# mypy only
from typing import Callable, Any


class InputField(metaclass=ABCMeta):
    """Abstract base for an input field of a console."""
    accept_callback: Callable[[str], Any]


class OutputField(metaclass=ABCMeta):
    """Abstract base for a multiline output field of a console."""

    @abstractmethod
    def write_line(self, text: str) -> None:
        pass


class Console:
    def __init__(self,
                 input_widget: InputField,
                 output_widget: OutputField,
                 *, echo: bool = True):
        self._input = input_widget
        self._output = output_widget

        # See python/mypy/#708
        self._input.accept_callback = self._input_handler  # type: ignore

        self.echo = echo
        self.commands: Queue[str] = Queue()

    def _input_handler(self, command: str):
        self.commands.put(command)
        if self.echo:
            self.print(command)

    def print(self, text: str) -> None:
        self._output.write_line(text)
