from abc import ABCMeta, abstractmethod
from queue import Queue

# mypy only
from .tui import TextArea
from typing import Callable, Any

# TODO: typehints

class InputField(metaclass=ABCMeta):
    """Abstract base for an input field of a console."""
    accept_callback: Callable[[str], Any]


class OutputField(metaclass=ABCMeta):
    """Abstract base for a multiline output field of a console."""

    @abstractmethod
    def write_line(self, text: str) -> None:
        pass


class TUIInputField(InputField):
    __slots__ = ('accept_callback', '_text_area')

    def __init__(self, text_area: TextArea):
        self.accept_callback: Callable[[str], Any] = lambda t: None

        self._text_area = text_area
        self._text_area.accept_handler = self._accept_input

    def _accept_input(self, buff):
        text = self._text_area.text
        self.accept_callback(text)


class TUIOutputField(OutputField):
    def __init__(self, text_area: TextArea):
        self._text_area = text_area

    def write_line(self, text):
        # TODO: Document is far too large of a class for what its used here.
        # Come up with something leaner
        from prompt_toolkit.document import Document
        new_text = self._text_area.text + '\n' + text
        self._text_area.document = Document(new_text, len(new_text))


class Console:
    def __init__(self,
                 input_widget: InputField,
                 output_widget: OutputField,
                 *, echo=True):
        self._input = input_widget
        self._output = output_widget

        # See python/mypy/#708
        self._input.accept_callback = self._input_handler  # type: ignore

        self.echo = echo
        self.commands = Queue()

    def _input_handler(self, command: str):
        self.commands.put(command)
        if self.echo:
            self.print(command)

    def print(self, text):
        self._output.write_line(text)
