from services.planner import overlap
from rich.console import Console
from rich.prompt import Prompt
from src.services.data_manager import add_event, RESOURCES
from rich.prompt import Confirm
from services.planner import is_new_event_overlapping_existing
from datetime import datetime
from rich.panel import Panel
from rich.text import Text

def command_add():
    console = Console()
    name = console.input("Nombre del evento: \n")
    desc = " "
    if Confirm.ask("Desea agregar descripción al evento? \n"):
        desc = console.input("Descripción del evento: \n")
    
    console.print("\n[bold cyan]Tipo de evento:[/bold cyan]")
    console.print("Seleccione, usando las teclas indicadas a continuación, el tipo de evento que desea crear: \n"
                  "")

    event_type = console.input("T")
    
    console.print("\n[bold cyan]Recursos dsiponibles:[/bold cyan]")
    for resource_id, resoruce_data in RESOURCES.items():
        console.print(f"{resource_id}: {resoruce_data.nombre}, casa {resoruce_data.house}")


    while True:
        console.print("\n[bold cyan]Fecha y hora de inicio del evento:[/bold cyan]")
        try:
            year_start = int(Prompt.ask("Año: \n"))
            month_start = int(Prompt.ask("Mes: \n"))
            day_start = int(Prompt.ask("Día: \n"))
            hour_start = int(Prompt.ask("Hora: \n", default=0))
            minute_start = int(Prompt.ask("Minutos: \n", default=0))        
        except ValueError as e:
            if "month" in str(e):
                print("[red] Error! mes inválido (debe ser 1-12) [red]")
            elif "day" in str(e):
                print("[red] Error! día inválido para el mes solicitado [red]")
            elif "hour" in str(e):
                print("[red] Error! hora inválida (debe ser 0-23) [red]")
            elif "minute" in str(e):
                print("[red] Error! minuto inválido (debe ser 0-59) [red]")
            else:
                print(f"Ups! entrada invalida.. Tipo de error: {type(e)}. Error: {e}")
            print("Inténtelo de nuevo :) \n")
            continue
        start_date = datetime(year_start, month_start, day_start, hour_start, minute_start)
        break

    while True:
        console.print("\n[bold cyan]Fecha y hora de fin del evento:[/bold cyan]")
        try:
            year_end = int(Prompt.ask("Año"))
            month_end = int(Prompt.ask("Mes [1-12]"))
            day_end = int(Prompt.ask("Día [1-30]"))
            hour_end = int(Prompt.ask("Hora [0-23]", default=0))
            minute_end = int(Prompt.ask("Minutos [0-59]", default=0))
        except ValueError as e:
            if "month" in str(e):
                print("[red] Error! mes inválido (debe ser 1-12) [red]")
            elif "day" in str(e):
                print("[red] Error! día inválido para el mes solicitado [red]")
            elif "hour" in str(e):
                print("[red] Error! hora inválida (debe ser 0-23) [red]")
            elif "minute" in str(e):
                print("[red] Error! minuto inválido (debe ser 0-59) [red]")
            else:
                print(f"[red] Ups! entrada inválida... Tipo de error: {type(e)}. Error: {e} [red]")
            print("Inténtelo de nuevo :)\n")
            continue
        end_date = datetime(year_end, month_end, day_end, hour_end, minute_end)
        break
    
    while True:
        if end_date <= start_date:
            raise ValueError("[red]La fecha final debe ser posterior a la inicial[/red]")
        
        break

    #!agregar aqui la llamada a la funcion is_new_event_overlapping_existing para ver si el evento se solapa con los guardados en el json
    is_new_event_overlapping_existing()
        
    add_event(name=name, description=desc, start=start_date, end=end_date)
    console.print(f"[green]Evento '{name}' agregado[/green]")

#AGREGAR LA LLAMADA A LA FUNCION FIND_NEXT_AVAILABLE_TIME_SLOT()