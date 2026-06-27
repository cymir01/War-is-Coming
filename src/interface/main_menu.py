from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from src.interface.command_add_event import command_add
from src.interface.command_list_events import command_list_planned_events
from src.interface.command_view_details import command_view_details
from src.interface.command_delete_event import command_delete_event
from src.services.data_manager import list_events

console = Console()

def main():
    panel = Panel(Text("¡War is Coming!", justify="center"), style="deep_sky_blue4")
    console.print(panel)
    user_name = Prompt.ask("¿Cuál es tu nombre?")
    console.print(f"Hola {user_name}!. A continuación los comandos para realizar acciones:")
    console.print(
        "[bold cyan]a[/bold cyan] - agregar evento\n"
        "[bold cyan]l[/bold cyan] - listar eventos\n"
        "[bold cyan]d[/bold cyan] - eliminar evento\n"
        "[bold cyan]v[/bold cyan] - ver detalles de un evento\n"
        "[bold cyan]s[/bold cyan] - salir\n"
    )

    while True:
        cmd = console.input(f"[bold cyan]¿Qué acción desea realizar {user_name}? [/bold cyan]\n").strip().lower()

        if cmd == 'a':
            command_add()
        elif cmd == 'l':
            events = list_events()
            if not events:
                console.print("[yellow]Todavía no hay eventos programados[/yellow]")
            else:
                command_list_planned_events()
        elif cmd == 'v':
            command_view_details()
        elif cmd == 'd':
            command_delete_event()
        elif cmd == 's':
            console.print(f"Adiós {user_name}! :(")
            break
        else:
            console.print("[red]Comando no reconocido. Inténtelo de nuevo :)[/red]")


# from rich.console import Console
# from rich.panel import Panel
# from rich.prompt import Prompt
# from rich.text import Text
# from src.services.data_manager import list_events, add_event
# from rich.prompt import Confirm
# from src.interface.command_add_event import command_add
# from src.interface.command_view_details import command_view_details
# from src.interface.command_list_events import command_list_planned_events
# from src.interface.command_delete_event import command_delete_event


# console = Console()

# panel = Panel(Text("¡War is Coming!", justify="center"), style="deep_sky_blue4")
# console.print(panel)
# user_name = Prompt.ask("¿Cuál es tu nombre?")
# #añadir un texto de bienvenida como Hola {user_name}, etc + la explicacion e los comandos para realizar acciones
# print(f"Hola {user_name}!. A continuacion los comandos pra realizar acciones...")
# print(
#     "a - agregar \n"
#     "l - listar \n"
#     "d - eliminar \n"
#     "v - ver detalles \n"
# )
# #!mejorar la interfaz para que perimita ejecutar comandos (agregar, listar, salir, eliminar evento) presionando ciertas teclas (a, l, s, e)
# #!agregar los siguientes comandos: agregar, listar + ver detalles (quiza usando el id como comando (ej: 5 para ver detalles de evento 5)), salir, eliminar evento
# while True:  
#     cmd = console.input(f"[bold cyan] ¿Qué acción desea realizar {user_name}? (explicar los comandos) [/bold cyan]\n")
    
#     if cmd == 'a' or 'A':
#         command_add()

#     elif cmd == 'l' or 'L':
#         events = list_events()
#         if not events: 
#             console.print(f"[yellow]Todavía no hay eventos programados {user_name}[/yellow]") 
#         else:
#             command_list_planned_events()

#     elif cmd == 'v' or 'V':
#         cmd_input = console.input(f"[bold cyan]Si desea ver detalles de un evento específico presione la tecla V[/bold cyan]\n")
#         if cmd_input == 'v' or 'V':
#                 command_view_details()

#     elif cmd == 'd' or 'D':
#         command_delete_event()

#     elif cmd == 's' or 'S': 
#         console.print(f"Adiós {user_name}! :(") 
#         break

#     else:
#         console.print("Comando no reconocido. Inténtelo de nuevo :)\n")