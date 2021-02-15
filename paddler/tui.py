from prompt_toolkit.widgets import TextArea, HorizontalLine
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Layout, VerticalAlign, ScrollablePane
from prompt_toolkit.layout.containers import (FloatContainer, HSplit, Window,
                                              Float)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import Application

style = Style(
    [
        ("output-field", "bg:#000044 #ffffff"),
        ("history-field", "bg:#000000 #ffffff"),
        ("input-field", "bg:#000000 #ffffff"),
        ("line", "#004400"),
        ("prompt", "fg:orange"),
        ("placeholder", "fg: grey"),
    ]
)


prompt = FormattedText([("class:prompt", ">>> ")])

history_field = TextArea(height=9, text='\n'*9)
input_field = TextArea(
    height=1,
    prompt=prompt,
    style="class:input-field",
    multiline=False,
    wrap_lines=False,
    # completer=completion,
    complete_while_typing=True
)

placeholder_text = "Nothing here yet. Type some commands and we'll see."
logs_placeholder = Window(content=FormattedTextControl(
    FormattedText([("class:placeholder", placeholder_text)])
))
log_items = ScrollablePane(HSplit([logs_placeholder]))

root_container = FloatContainer(
    content=HSplit([
        log_items,
        HorizontalLine(),
        history_field,
        input_field
    ], align=VerticalAlign.BOTTOM),
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=16, scroll_offset=1),
        )
    ],
)

key_bindings = KeyBindings()
layout = Layout(root_container, focused_element=input_field)
app: Application = Application(layout, full_screen=True, style=style,
                               key_bindings=key_bindings)


@key_bindings.add('c-q')
@key_bindings.add('c-d')
@key_bindings.add('c-c')
def kb_exit_(_):
    """Press Ctrl-Q, Ctrl-D, or Ctrl-C to exit."""
    app.exit()
