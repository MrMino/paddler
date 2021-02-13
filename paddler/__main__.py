from .tui import app, input_field, history_field
from .console import Console, TUIInputField, TUIOutputField


Console(
    TUIInputField(input_field), TUIOutputField(history_field)
)

app.run()
