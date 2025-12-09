from rich.table import Table
from rich.console import Console

# while True:
#     try:
#         events = {
#             "1": {
#                 "desc": "tarea",
#                 "estado": "pendiente"
#             }
#         }
#         cmd = input("id \n")
#         id = events[cmd]
#         print(id)
#         break
#     except Exception:
#         print("mal")

# events = {
#             "1": {
#                 "desc": "tarea",
#                 "estado": "pendiente"
#             }
#         }
# cmd = input("id \n")
# id = events.get(cmd, "no existe el evento solicitado")
# print(id)

# alumno = {
#     'nombre': 'Ana', #key: value
#     'id_matricula': 12345, 
#     'curso_actual': 'Programación I', 
#     "activa": True
#     }

# nombre = alumno.get('nombre', 'no especificado')

# print(nombre)
console = Console()
events = {
        "1": {
            "desc": "tarea",
            "estado": "pendiente"
        }
    }
cmd = input("Introduzca el ID del evento para mostrar los detalles \n")

while True:
    try:
        if cmd in events:
            table = Table(title=f"Detalles del evento número {cmd}")
            table.add_column("ID", style="cyan")
            table.add_column("Descripción", style="magenta")
            table.add_column("Estado", style="green")

        for id, event in events.items():
            if cmd == id:
                table.add_row(str(id), event['desc'], event['estado'])

        console.print(table)

    except Exception:
        print("El evento solicitado no existe")
        continue
    
    break