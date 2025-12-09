from rich.table import Table
from rich.console import Console

console = Console()
events = {
        "1": {
            "desc": "tarea",
            "estado": "pendiente"
        }
    }

while True:
    cmd = input("Introduzca el ID del evento para mostrar los detalles o presione la tecla S para salir\n")
    if cmd.lower() == 's':
        break

    if cmd in events:
        event = events[cmd]
        table = Table(title=f"Detalles del evento número {cmd}")
        table.add_column("ID", style="cyan")
        table.add_column("Descripción", style="magenta")
        table.add_column("Estado", style="green")
        table.add_row(cmd, event['desc'], event['estado'])
        console.print(table)
        break
    
    else:
        console.print("[red]El evento solicitado no existe[/red]")

#!estudiar el flujo de ejecucion de este codigo
# while True:
#     try:
#         if cmd in events:
#             table = Table(title=f"Detalles del evento número {cmd}")
#             table.add_column("ID", style="cyan")
#             table.add_column("Descripción", style="magenta")
#             table.add_column("Estado", style="green")

#         for id, event in events.items():
#             if cmd == id:
#                 table.add_row(str(id), event['desc'], event['estado'])

#         console.print(table)

#     except Exception:
#         print("El evento solicitado no existe")
#         continue
    
#     break

