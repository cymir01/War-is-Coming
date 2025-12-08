from date_validation import overlap
from date_validation import validate_datetime_input
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from core import add_event, list_events
from rich.prompt import Confirm
from interface.command_add_event import command_add
from interface.command_view_details import command_view_details

console = Console()

#!usar los ids de los eventos para mostrar los detalles de los eventos usandolos de comando
def command_view_details():
    events = list_events()
    cmd = console.input("Introduzca el número del evento para mostrar los detalles")
    table = Table(title="Detalles del evento")
    table.add_column("ID", style="cyan")
    table.add_column("Descripción", style="magenta")
    table.add_column("Estado", style="green")

    for id, event in events.items():
        if cmd == id:
            table.add_row(str(id), event['desc'], events['estado'])
    