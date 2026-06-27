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
    event_type = Prompt.ask("Tipo de evento:", choices=event_types) #ver como manejar el default
    
    location = None
    if Confirm.ask("Desea especificar una locación para el evento?"):
        location = console.input("Ubicación:")

    console.print("\n[bold cyan]Recursos dsiponibles:[/bold cyan]")
    for resource_id, resoruce_data in RESOURCES.items():
        type = resoruce_data.resource_type if resoruce_data.resource_type is not None else "sin tipo"
        house = resoruce_data.house if resoruce_data.house is not None else "sin casa"
        console.print(f"{resource_id}: {resoruce_data.name} (tipo: {type}, casa: {house})")

    resources_input = Prompt.ask("Ingrese los ids de los recursos que desea separados por comas", default = "")
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
    
    def ask_datetime(prompt):
        while True:
            try:
                year = int(Prompt.ask(f"Año - {prompt}"))
                month = int(Prompt.ask(f"Mes - {prompt}"))
                day = int(Prompt.ask(f"Día - {prompt}"))
                hour = int(Prompt.ask(f"Hora - {prompt}"))
                minute = int(Prompt.ask(f"Minuto - {prompt}"))
                return datetime(year, month, day, hour, minute)
            except ValueError:
                console.print("[red]ups! error en la fecha. Inténtelo de nuevo[/red]")
            start = ask_datetime("Inicio")
            end = ask_datetime("Fin")
            if end <= start:
                console.print("[red]La fecha final debe ser posterior a la inicial[/red]")
                return
        
    if Confirm.ask("Desea buscar el próximo hueco disponible para estos recursos?"):
        duration = (end_date - start_date).total_seconds() / 3600.0
        slot = find_next_available_time_slot(resources_ids, duration, start_from=start_date)
        if slot:
            start_date, end_date = slot
            console.print(f"[green]Hueco encontrado: {start_date} - {end_date}[/green]")
            if not Confirm.ask("Desea usar este hueco?"):
                return
        else:
            console.print("[red]No se encontró un hueco disponible en los próximos días[/red]")
            return

    ok, result = add_event(name, desc, start_date, end_date, event_type, location, resources_ids)
    if ok:
        console.print(f"[green]Evento '{name}' agregado con ID: {result}[/green]")
    else:
        console.print(f"[red]Error: {result}[/red]")
        
    # add_event(name=name, description=desc, start=start_date, end=end_date)
    # console.print(f"[green]Evento '{name}' agregado[/green]")

#AGREGAR LA LLAMADA A LA FUNCION FIND_NEXT_AVAILABLE_TIME_SLOT()