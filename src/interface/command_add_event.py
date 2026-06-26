from rich.console import Console
from rich.prompt import Prompt, Confirm
from datetime import datetime
from src.services.data_manager import add_event, RESOURCES
from src.services.planner import find_next_available_time_slot

def command_add():
    console = Console()
    console.print("\n[bold cyan]Agregar nuevo evento[/bold cyan]")
    
    name = console.input("Nombre del evento: \n")
    desc = None
    if Confirm.ask("Desea agregar descripción al evento? \n"):
        desc = console.input("Descripción del evento: \n")
    
    event_types = ["Asedio", "Batalla Naval", "Asalto", "Defensa", "Emboscada", "Batalla Campal"]
    console.print("\nTipos de evento disponibles: Asedio, Batalla Naval, Asalto, Defensa, Emboscada, Batalla Campal")
    event_type = Prompt.ask("Tipo de evento:", choices=event_types, default="Batalla campal")
    
    location = None
    if Confirm.ask("Desea especificar una locación para el evento?"):
        location = console.input("Ubicación:")

    console.print("\n[bold cyan]Recursos dsiponibles:[/bold cyan]")
    for resource_id, resoruce_data in RESOURCES.items():
        type = resoruce_data.resource_type if resoruce_data.resource_type is not None else "sin tipo"
        house = resoruce_data.house if resoruce_data.house is not None else "sin casa"
        console.print(f"{resource_id}: {resoruce_data.name} (tipo: {type}, casa: {house})")

    resources_input = Prompt.ask("ids de recursos (separados por comas)", default = "")
    resources_ids = []
    if resources_input.strip():
        try:
            separated_ids = resources_input.split(",")
            for id in separated_ids:
                if id.strip():
                    resources_ids.append(int(id.strip()))
        except ValueError:
            console.print("[red]ids inválidos. Deben ser números[/red]")
            return
        
#corregir los while para las fechas, no manejan bien los errores (valida los rangos manualmente) + encapsular
    while True:
        console.print("\n[bold cyan]Fecha y hora de inicio del evento:[/bold cyan]")
        try:
            year_start = int(Prompt.ask("Año"))
            month_start = int(Prompt.ask("Mes [1-12]"))
            day_start = int(Prompt.ask("Día [1-31]"))
            hour_start = int(Prompt.ask("Hora [0-23]"))
            minute_start = int(Prompt.ask("Minutos [0-59]"))
        except ValueError:
            console.print("[red]Error: entrada invalida.. ingrese números enteros[/red]")
            continue
        if month_start < 1 or month_start > 12:
            console.print("[red]Error: mes inválido (debe ser 1-12)[/red]")
            continue
        if day_start < 1 or day_start > 31:
            console.print("[red]Error: día inválido (debe ser 1-31)[/red]")
            continue
        if hour_start < 0 or hour_start > 23:
            console.print("[red]Error: hora inválida (debe ser 0-23)[/red]")
            continue
        if minute_start < 0 or minute_start > 59:
            console.print("[red]Error: minuto inválido (debe ser 0-59)[/red]")
            continue
        try:
            start_date = datetime(year_start, month_start, day_start, hour_start, minute_start)
            break
        except ValueError:
            console.print("[red]Error: fecha inválida[/red]")
            continue

    while True:
        if end_date <= start_date:
            console.print("[red]Error: la fecha final debe ser posterior a la inicial[/red]")
            console.print("\n[red] Reingrese la fecha y hora de fin[red]")
            while True:
                console.print("\n[bold cyan]Fecha y hora de fin del evento:[/bold cyan]")
                try:
                    year_end = int(Prompt.ask("Año"))
                    month_end = int(Prompt.ask("Mes [1-12]"))
                    day_end = int(Prompt.ask("Día [1-31]"))
                    hour_end = int(Prompt.ask("Hora [0-23]"))
                    minute_end = int(Prompt.ask("Minutos [0-59]"))
                except ValueError:
                    console.print("[red]Error: entrada invalida, ingrese numeros enteros[/red]")
                    continue

                if month_end < 1 or month_end > 12:
                    console.print("[red]Error: mes inválido (debe ser 1-12)[/red]")
                    continue
                if day_end < 1 or day_end > 31:
                    console.print("[red]Error: día inválido (debe ser 1-31)[/red]")
                    continue
                if hour_end < 0 or hour_end > 23:
                    console.print("[red]Error: hora inválida (debe ser 0-23)[/red]")
                    continue
                if minute_end < 0 or minute_end > 59:
                    console.print("[red]Error: minuto inválido (debe ser 0-59)[/red]")
                    continue

                try:
                    end_date = datetime(year_end, month_end, day_end, hour_end, minute_end)
                    break
                except ValueError:
                    console.print("[red]fecha inválida[/red]")
                    continue
            continue
        else:
            break
    
    if Confirm.ask("Desea buscar el próximo hueco disponible para estos recursos?"):
        duration = (end_date - start_date).total_seconds() / 3600.0
        slot = find_next_available_time_slot(resources_ids, duration, start_from=start_date)
        if slot:
            start_date, end_date = slot
            console.print(f"[green]Hueco encontrado: {start_date} - {end_date}[/green]")
            if not Confirm.ask("Usar este hueco?"):
                return
        else:
            console.print("[red]No se encontró un hueco disponible en los próximos días[/red]")
            return

    ok, result = add_event(name, desc, start_date, end_date, event_type, location, resources_ids)
    if ok:
        console.print(f"[green]Evento '{name}' agregado con ID {result}[/green]")
    else:
        console.print(f"[red]Error: {result}[/red]")
        
    # add_event(name=name, description=desc, start=start_date, end=end_date)
    # console.print(f"[green]Evento '{name}' agregado[/green]")

#AGREGAR LA LLAMADA A LA FUNCION FIND_NEXT_AVAILABLE_TIME_SLOT()