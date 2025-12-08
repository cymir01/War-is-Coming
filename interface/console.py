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

panel = Panel(Text("¡War is Coming!", justify="center"), style="deep_sky_blue4")
console.print(panel)
user_name = Prompt.ask("¿Cuál es tu nombre, lord?")
#!perimitir que los minutos tengan valor por defecto " "

#!mejorar la interfaz para que perimita ejecutar comandos (agregar, listar, salir, eliminar evento) presionando ciertas teclas (a, l, s, e)
#!agregar los siguientes comandos: agregar, listar + ver detalles (quiza usando el id como comando (ej: 5 para ver detalles de evento 5)), salir, eliminar evento
while True:  
    cmd = console.input(f"[bold cyan]¿Hola {user_name}!, qué acción desea realizar? (agregar, ): [/bold cyan]\n")
    if cmd == 'a' or 'A':
        command_add()
    elif cmd == 'l' or 'L':
        events = list_events()
        if not events: 
            console.print("[yellow]Todavía no hay eventos programados[/yellow]") 
        else:
            table = Table(title="Lista de Eventos") 
            table.add_column("ID", style="cyan") 
            table.add_column("Descripción", style="magenta") 
            table.add_column("Estado", style="green")  
            
            #!agregar mas info de los eventos a la tabla
            for id, event in events.items(): 
                table.add_row(str(id), event['desc'], events['estado'])
            
            console.print(table)
            cmd_input = console.input(f"[bold cyan]Si desea ver detalles de un evento específico presione la tecla V[/bold cyan]\n")
            if cmd_input == 'v' or 'V':
                command_view_details()


    elif cmd == 's' or 'S': 
        console.print(f"Adiós {user_name}!") 
        break

    else:
        console.print("Comando no reconocido. Vuelva a intentarlo\n")

#!usar estas tablas para listar el inventario de recursos y eventos y demas
# tabla = Table(title="Ejércitos de Poniente")
# tabla.add_column("Casa", style="cyan")
# tabla.add_column("Líder", style="magenta")
# tabla.add_column("Tropas", justify="right")
# tabla.add_row("Stark", "Robb Stark", "20,000")
# tabla.add_row("Lannister", "Tywin Lannister", "35,000")
# console.print(tabla)