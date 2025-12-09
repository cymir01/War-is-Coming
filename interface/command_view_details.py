from rich.console import Console
from rich.table import Table
from rich.text import Text
from services.core import list_events

#!Bug Report: (revisar por que ocurre el error)
# cymir@cymir-ThinkPad-T440p:~/00 Pojects/War-is-Coming$ /bin/python3 "/home/cymir/00 Pojects/War-is-Coming/interface/command_view_details.py"
# Traceback (most recent call last):
#   File "/home/cymir/00 Pojects/War-is-Coming/interface/command_view_details.py", line 4, in <module>
#     from core import list_events
# ModuleNotFoundError: No module named 'core'

console = Console()

#!usar los ids de los eventos para mostrar los detalles de los eventos usandolos de comando
def command_view_details():
    events = list_events()
    while True:
        cmd = console.input("Introduzca el ID del evento para mostrar los detalles o presione la tecla s para salir")

        if cmd.lower() == 's':
            break

        if cmd in events:
            table = Table(title=f"Detalles del evento número {cmd}")
            table.add_column("ID", style="cyan")
            table.add_column("Descripción", style="magenta")
            table.add_column("Estado", style="green")
            table.add_row(cmd, events['desc'], events['estado']) #!agregar aqui mas info del evento (recursos que usa, etc)
            console.print(table)
            break
        else:
            console.print("[red]El evento solicitado no existe[/red]")