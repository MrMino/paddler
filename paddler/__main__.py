from .tui import app, input_field, history_field
from .tui.controls import TUIInputField, TUIOutputField
from .console import Console


Console(
    TUIInputField(input_field), TUIOutputField(history_field)
)

app.run()
