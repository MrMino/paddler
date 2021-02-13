from queue import Queue

# mypy only
from .tui import TextArea
from typing import Callable, Any

# TODO: typehints


# TODO: abstract class
class TUIInputField:
    __slots__ = ('accept_callback', '_text_area')

    def __init__(self, text_area: TextArea):
        self.accept_callback: Callable[[str], Any] = lambda t: None

        self._text_area = text_area
        self._text_area.accept_handler = self._accept_input

    def _accept_input(self, buff):
        text = self._text_area.text
        self.accept_callback(text)


# TODO: abstract class
class TUIOutputField:
    def __init__(self, text_area: TextArea):
        self._text_area = text_area

    def write_line(self, text):
        # TODO: Document is far too large of a class for what its used here.
        # Come up with something leaner
        from prompt_toolkit.document import Document
        new_text = self._text_area.text + '\n' + text
        self._text_area.document = Document(new_text, len(new_text))


class Console:
    def __init__(self, input_widget, output_widget, *, echo=True):
        self._input = input_widget
        self._output = output_widget

        self._input.accept_callback = self._input_handler

        self.echo = echo
        self.commands = Queue()

    def _input_handler(self, command: str):
        self.commands.put(command)
        if self.echo:
            self.print(command)

    def print(self, text):
        self._output.write_line(text)
