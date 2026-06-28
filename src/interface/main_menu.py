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
    user_name = Prompt.ask("¿Cuál es su nombre, milord?")
    console.print(f"Hola {user_name}!. Bienvenid@ al planficiador de eventos bélicos de Poniente")

    while True:
        console.print("\nA continuación los comandos para realizar acciones en el planificador: ")
        console.print(
        "[bold cyan]a[/bold cyan] - agregar evento\n"
        "[bold cyan]l[/bold cyan] - listar eventos\n"
        "[bold cyan]d[/bold cyan] - eliminar evento\n"
        "[bold cyan]v[/bold cyan] - ver detalles de un evento o recurso\n"
        "[bold cyan]s[/bold cyan] - salir\n"
        )

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