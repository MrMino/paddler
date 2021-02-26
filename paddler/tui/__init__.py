from prompt_toolkit.widgets import TextArea, HorizontalLine
from prompt_toolkit.widgets import Label
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Layout, ScrollablePane
from prompt_toolkit.layout.containers import (FloatContainer, HSplit, Float)
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import Application
from prompt_toolkit.widgets import Box, Shadow, Frame
from prompt_toolkit.layout import ConditionalContainer
from prompt_toolkit.filters import Condition


style = Style(
    [
        ("output-field", "bg:#000044 #ffffff"),
        ("history-field", "bg:#000000 #ffffff"),
        ("input-field", "bg:#000000 #ffffff"),
        ("line", "#004400"),
        ("prompt", "fg:orange"),
        ("placeholder", "grey"),
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

placeholder_text = (
    "Nothing here yet:\n"
    " - Type \"help\" to see available commands.\n"
    " - Press \"?\" for the list of keybindings."
)
logs_placeholder = Label(
    FormattedText([("class:placeholder", placeholder_text)])
)

log_items = HSplit([logs_placeholder])
log_pane = ScrollablePane(log_items)

show_kb_help = False
bindings_help = ConditionalContainer(
    Box(Shadow(Frame(Label(""), "Key bindings:"))),
    filter=Condition(lambda: show_kb_help)
)

root_container = FloatContainer(
    content=HSplit([
        log_pane,
        HorizontalLine(),
        history_field,
        input_field
    ]),
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=16, scroll_offset=1),
        ),
        Float(bindings_help),
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
    """Exit"""
    app.exit()


@key_bindings.add('c-i')
def kb_ipdb_(_):
    """Run debugger"""
    breakpoint()


@key_bindings.add('c-t')
def kb_test_(_):
    """Test method"""


@key_bindings.add('?')
def kb_bindings_help_(_):
    """Show this window"""
    global show_kb_help
    show_kb_help = not show_kb_help
