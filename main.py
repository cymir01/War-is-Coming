from date_validation import overlap
from date_validation import validate_datetime_input
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from core import add_event, list_events
from rich.prompt import Confirm

console = Console()

panel = Panel(Text("¡War is Coming!", justify="center"), style="deep_sky_blue4")
console.print(panel)
user_name = Prompt.ask("¿Cuál es tu nombre, lord?")
#!perimitir que los minutos tengan valor por defecto " "

#!mejorar la interfaz para que perimita ejecutar comandos (agregar, listar, salir, eliminar evento)
#!presionando ciertas teclas (a, l, s, e)
while True:  
    cmd = console.input(f"[bold cyan]¿Hola {user_name}!, qué acción desea realizar? (agregar, ): [/bold cyan]\n")
    if cmd == 'a':
        name = console.input("Nombre del evento: \n")
        desc = " "
        if Confirm.ask("Desea agregar descripción al evento? \n"):
            desc = console.input("Descripción del evento: \n")
        
        console.print("\n[bold cyan]Era histórica del evento:[/bold cyan]")
        while True:
            era_input = Prompt.ask("¿Antes de la Conquista (AC) o después de la Conquista (DC)?")
            era = era_input.strip().upper()
            if era in ("AC", "DC"):
                break
            else:
                console.print("[red]Por favor, ingrese 'AC' o 'DC'.[/red]")
    
        while True:
            console.print("\n[bold cyan]Fecha y hora de inicio del evento:[/bold cyan]")
            try:
                year_s = int(Prompt.ask("Año", default=0)) 
                #!revisar bien por que se produce el bucle infinito en la linea 40 al pone type solo o con default
                month_s = int(Prompt.ask("Mes [1-12]"))
                day_s = int(Prompt.ask("Día [1-30]"))
                hour_s = int(Prompt.ask("Hora [0-23]", default=0, type=int))
                minute_s = int(Prompt.ask("Minutos [0-59]", default=0, type=int))
            except Exception:
                console.print("[red]❌ Entrada inválida. Use solo números.[/red]")
                continue

            console.print("\n[bold cyan]Fecha y hora de fin del evento:[/bold cyan]")
            try:
                year_e = int(Prompt.ask("Año"))
                month_e = int(Prompt.ask("Mes [1-12]"))
                day_e = int(Prompt.ask("Día [1-30]"))
                hour_e = int(Prompt.ask("Hora [0-23]", default=0))
                minute_e = int(Prompt.ask("Minutos [0-59]", default=0))
            except Exception:
                console.print("[red]❌ Entrada inválida. Use solo números.[/red]")
                continue
            
            ok_s, msg_s, start = validate_datetime_input(year_s, month_s, day_s, hour_s, minute_s, era)
            if not ok_s:
                console.print(f"[red]{msg_s}[/red]")
                continue  # ← vuelve a pedir SOLO las fechas

            ok_e, msg_e, end = validate_datetime_input(year_e, month_e, day_e, hour_e, minute_e, era)
            if not ok_e:
                console.print(f"[red]{msg_e}[/red]")
                continue  # ← vuelve a pedir SOLO las fechas
        
            #!no me interesa que itere de nuevo desde el principio, sino solo a partir de la parte en la que agrega las fechas
            if end <= start:
                console.print("[red]❌ La fecha final debe ser posterior a la inicial.[/red]")
                continue  # ← vuelve a pedir SOLO las fechas
            break
        add_event(name=name, description=desc, start=start, end=end, era=era)
        console.print(f"[green]✅ Evento '{name}' agregado.[/green]")

        #!agregar aqui la llamada a la funcion is_new_event_overlapping_existing para ver si el evento se solapa con los guardados en el json

    elif cmd == 'l':
        events = list_events()
        if not events: 
            console.print("[yellow]Todavía no hay eventos programados[/yellow]") 
        else:
            table = Table(title="Lista de Eventos") 
            table.add_column("ID", style="cyan") 
            table.add_column("Descripción", style="magenta") 
            table.add_column("Estado", style="green")  
            
            for id, event in events.items(): 
                table.add_row(str(id), event['desc'], events['estado'])  
            
            console.print(table)

    elif cmd == 's': 
        console.print(f"Adiós {user_name}!") 
        break

    else:
        console.print("Comando no reconocido\n")

#!usar estas tablas para listar el inventario de recursos y eventos y demas
# tabla = Table(title="Ejércitos de Poniente")
# tabla.add_column("Casa", style="cyan")
# tabla.add_column("Líder", style="magenta")
# tabla.add_column("Tropas", justify="right")
# tabla.add_row("Stark", "Robb Stark", "20,000")
# tabla.add_row("Lannister", "Tywin Lannister", "35,000")
# console.print(tabla)