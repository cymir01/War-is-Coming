from services.date_validation import overlap
from services.date_validation import validate_datetime_input
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from services.core import add_event, list_events
from rich.prompt import Confirm
from services.date_validation import is_new_event_overlapping_existing

def command_add():
    console = Console()
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
    #!ver por que ocurren problemas al usar type=int, hacer varias pruebas e investigar
    while True:
        console.print("\n[bold cyan]Fecha y hora de inicio del evento:[/bold cyan]")
        try:
            year_s = int(Prompt.ask("Año")) 
            #!revisar bien por que se produce el bucle infinito en la linea 40 al poner type=int solo o con default=0
            month_s = int(Prompt.ask("Mes [1-12]"))
            day_s = int(Prompt.ask("Día [1-30]"))
            hour_s = int(Prompt.ask("Hora [0-23]", default=0))
            minute_s = int(Prompt.ask("Minutos [0-59]", default=0))
        except Exception:
            console.print("[red]Entrada inválida. Use solo números[/red]")
            continue

        console.print("\n[bold cyan]Fecha y hora de fin del evento:[/bold cyan]")
        try:
            year_e = int(Prompt.ask("Año"))
            month_e = int(Prompt.ask("Mes [1-12]"))
            day_e = int(Prompt.ask("Día [1-30]"))
            hour_e = int(Prompt.ask("Hora [0-23]", default=0))
            minute_e = int(Prompt.ask("Minutos [0-59]", default=0))
        except Exception:
            console.print("[red]Entrada inválida. Use solo números.[/red]")
            continue
        
        ok_s, msg_s, start = validate_datetime_input(year_s, month_s, day_s, hour_s, minute_s, era)
        if not ok_s:
            console.print(f"[red]{msg_s}[/red]")
            continue  # ← vuelve a pedir SOLO las fechas

        ok_e, msg_e, end = validate_datetime_input(year_e, month_e, day_e, hour_e, minute_e, era)
        if not ok_e:
            console.print(f"[red]{msg_e}[/red]")
            continue  # ← vuelve a pedir SOLO las fechas

        if end <= start:
            console.print("[red]La fecha final debe ser posterior a la inicial.[/red]")
            continue  # ← vuelve a pedir SOLO las fechas

        #!agregar aqui la llamada a la funcion is_new_event_overlapping_existing para ver si el evento se solapa con los guardados en el json
        is_new_event_overlapping_existing()
        
        break
    add_event(name=name, description=desc, start=start, end=end, era=era)
    console.print(f"[green]Evento '{name}' agregado[/green]")