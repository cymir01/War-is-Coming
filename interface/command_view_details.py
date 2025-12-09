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
    cmd = console.input("Introduzca el ID del evento para mostrar los detalles")
    while True:
        try:
            if cmd in events:
                table = Table(title=f"Detalles del evento número {cmd}")
                table.add_column("ID", style="cyan")
                table.add_column("Descripción", style="magenta")
                table.add_column("Estado", style="green")
            else:
                print("El evento solicitado no existe")

            for id, event in events.items():
                if cmd == id:
                    table.add_row(str(id), event['desc'], event['estado'])
            
            console.print(table)

        except Exception:
            print("El evento solicitado no existe. Vuelva a intentarlo")
        break