from services.validation_logic import overlap
from services.validation_logic import validate_date_input
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from services.data_manager import add_event, list_events
from rich.prompt import Confirm
from services.validation_logic import is_new_event_overlapping_existing

def command_add():
    console = Console()
    name = console.input("Nombre del evento: \n")
    desc = " "
    if Confirm.ask("Desea agregar descripción al evento? \n"):
        desc = console.input("Descripción del evento: \n")

    while True:
        console.print("\n[bold cyan]Fecha y hora de inicio del evento:[/bold cyan]")
        try:
            year_start = int(Prompt.ask("Año"))
            month_start = int(Prompt.ask("Mes [1-12]"))
            day_start = int(Prompt.ask("Día [1-30]"))
            hour_start = int(Prompt.ask("Hora [0-23]", default=0))
            minute_start = int(Prompt.ask("Minutos [0-59]", default=0))
        except Exception:
            console.print("[red]Entrada inválida[/red]")
            continue

        bool_sart, msg_start, start_time = validate_date_input(year_start, month_start, day_start, hour_start, minute_start)
        if not bool_sart:
            console.print(f"[red]{msg_start}[/red]")
            continue
        break

    while True:
        console.print("\n[bold cyan]Fecha y hora de fin del evento:[/bold cyan]")
        try:
            year_end = int(Prompt.ask("Año"))
            month_end = int(Prompt.ask("Mes [1-12]"))
            day_end = int(Prompt.ask("Día [1-30]"))
            hour_end = int(Prompt.ask("Hora [0-23]", default=0))
            minute_end = int(Prompt.ask("Minutos [0-59]", default=0))
        except Exception:
            console.print("[red]Entrada inválida[/red]")
            continue

        bool_end, msg_end, end_time = validate_date_input(year_end, month_end, day_end, hour_end, minute_end)
        if not bool_end:
            console.print(f"[red]{msg_end}[/red]")
            continue

        if end_time <= start_time:
            console.print("[red]La fecha final debe ser posterior a la inicial.[/red]")
            continue
        break

    #!agregar aqui la llamada a la funcion is_new_event_overlapping_existing para ver si el evento se solapa con los guardados en el json
    is_new_event_overlapping_existing()
        
    add_event(name=name, description=desc, start=start_time, end=end_time)
    console.print(f"[green]Evento '{name}' agregado[/green]")

#AGREGAR LA LLAMADA A LA FUNCION FIND_NEXT_AVAILABLE_TIME_SLOT()