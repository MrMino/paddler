"""
Higher-level control classes for TUI components.
"""
from ..console import InputField, OutputField
from . import TextArea

from typing import Callable, Any


class TUIInputField(InputField):
    __slots__ = ('accept_callback', '_text_area')

    def __init__(self, text_area: TextArea):
        self.accept_callback: Callable[[str], Any] = lambda t: None

        self._text_area = text_area
        self._text_area.accept_handler = self._accept_input

    def _accept_input(self, _):
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
