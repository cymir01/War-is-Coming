from rich.console import Console
from rich.table import Table
from rich.text import Text
from core import list_events

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
    cmd = console.input("Introduzca el número del evento para mostrar los detalles")
    id = events[cmd] #!ejecutar y ver si esto funciona
    table = Table(title=f"Detalles del evento {id}")
    table.add_column("ID", style="cyan")
    table.add_column("Descripción", style="magenta")
    table.add_column("Estado", style="green")

    # for id, event in events.items():
    #     if cmd == id:
    #         table.add_row(str(id), event['desc'], events['estado'])
    
command_view_details()