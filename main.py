import datetime
from date_validation import overlap
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from core import add_event, list_events
from rich.prompt import Confirm
from date_validation import valid_year_westeros

console = Console()

panel = Panel(Text("¡War is Coming!", justify="center"), style="deep_sky_blue4")
console.print(panel)
user_name = Prompt.ask("¿Cuál es tu nombre, lord?")
#!perimitir que los minutos tengan valor por defecto " "

#!mejorar la interfaz para que perimita ejecutar comandos (agregar, listar, salir, eliminar evento)
#!presionando ciertas teclas (a, l, s, e)
while True:  
    cmd = console.input(f"[bold cyan]¿Hola {user_name}!, qué acción desea realizar? (agregar, ): [/bold cyan]\n")
    if cmd == 'agregar':
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
        
        console.print("\n[bold cyan]Ingrese la fecha y hora inicial del evento:[/bold cyan]")

        while True:
            try:
                day_start = int(console.input("Día: "))
                month_start = int(console.input("Mes: "))
                year_start = int(console.input("Año: "))
                hours_start = int(console.input("Hora: "))
                minutes_start = int(console.input("Minutos: "))

                if not (1 <= month_start <= 12):
                    console.print("[red]Mes inválido. Debe estar entre 1 y 12.[/red]")
                    continue
                if not (1 <= day_start <= 30):  # Validación básica, datetime validará días específicos
                    console.print("[red]Día inválido. Debe estar entre 1 y 30.[/red]")
                    continue
                if not (0 <= hours_start <= 23):
                    console.print("[red]Hora inválida. Debe estar entre 0 y 23.[/red]")
                    continue
                if not (0 <= minutes_start <= 59):
                    console.print("[red]Minutos inválidos. Debe estar entre 0 y 59.[/red]")
                    continue

                start = datetime.datetime(year_start, month_start, day_start, hours_start, minutes_start)

                if valid_year_westeros(year_start, era):
                    break
                else:
                    console.print("[red]Fecha inválida según el calendario de Poniente. Intente de nuevo.[/red]")
            except ValueError as e:
                console.print(f"[red]Error de fecha: {str(e)}. Intente de nuevo.[/red]")

        console.print("\n[bold cyan]Ingrese la fecha y hora final del evento:[/bold cyan]")
        
        while True:
            try:
                day_end = int(console.input("Día: "))
                month_end = int(console.input("Mes: "))
                year_end = int(console.input("Año: "))
                hours_end = int(console.input("Hora: "))
                minutes_end = int(console.input("Minutos: "))

                if not (1 <= month_end <= 12):
                    console.print("[red]Mes inválido. Debe estar entre 1 y 12.[/red]")
                    continue
                if not (1 <= day_end <= 30):
                    console.print("[red]Día inválido. Debe estar entre 1 y 30.[/red]")
                    continue
                if not (0 <= hours_end <= 23):
                    console.print("[red]Hora inválida. Debe estar entre 0 y 23.[/red]")
                    continue
                if not (0 <= minutes_end <= 59):
                    console.print("[red]Minutos inválidos. Debe estar entre 0 y 59.[/red]")
                    continue
                
                end = datetime.datetime(year_end, month_end, day_end, hours_end, minutes_end)

                if valid_year_westeros(year_end, era):
                    break
                else:
                    console.print("[red]Fecha inválida según el calendario de Poniente. Intente de nuevo.[/red]")
            except ValueError as e:
                console.print(f"[red]Error de fecha: {str(e)}. Intente de nuevo.[/red]")
        
        #!no me interesa que itere de nuevo desde el principio, sino solo a partir de la parte en la que agrega las fechas
        if end <= start:
            console.print("[red]Error: La fecha final debe ser posterior a la fecha inicial.[/red]")
            continue

        #!agregar aqui la llamada a la funcion is_new_event_overlapping_existing para ver si el evento se solapa
        #!con los guardados en el json

        add_event(name=name, description=desc, start=start, end=end)

    elif cmd == 'listar':
        events = list_events()
        if not events: 
            console.print("[yellow]No hay eventos programados[/yellow]") 
        else:
            table = Table(title="Lista de Eventos") 
            table.add_column("ID", style="cyan") 
            table.add_column("Descripción", style="magenta") 
            table.add_column("Estado", style="green")  
            
            for id, event in events.items(): 
                table.add_row(str(id), event['desc'], events['estado'])  
            
            console.print(table)
    elif cmd == 'salir': 
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