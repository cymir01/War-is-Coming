from rich.console import Console
from rich.prompt import Prompt, Confirm
from datetime import datetime
from src.services.data_manager import add_event, RESOURCES, RESTRICTIONS, list_events
from src.services.planner import find_next_available_time_slot

#AGREGAR DESPUES DEL TIPO DE EVENTO LA LISTA DE RECURSOS QUE REQUIERE
#MEJORAR LA VISUALIZACION DE RECURSOS, EN LUGAR DE LISTARLOS TODOS, PEDIR CASA Y LISTAR LOS RECURSOS POR CASA, ETC


def command_add():
    console = Console()
    console.print("\n[bold cyan]Agregar nuevo evento[/bold cyan]")
    
    name = console.input("Nombre del evento: \n")
    desc = None
    if Confirm.ask("\nDesea agregar descripción al evento? \n"):
        desc = console.input("Descripción del evento: \n")
    
    event_types = ["Asedio", "Batalla naval", "Asalto", "Defensa", "Emboscada", "Batalla campal", "Misión diplomática"]
    console.print("\nTipos de evento disponibles: Asedio, Batalla naval, Asalto, Defensa, Emboscada, Batalla campal y Misión diplomática")
    event_type = Prompt.ask("Tipo de evento:", choices=event_types)
    
    location = None
    if Confirm.ask("\n¿Desea especificar una locación para el evento?"):
        location = console.input("Ubicación:")

    console.print("\n[bold cyan]Era histórica[/bold cyan]")
    console.print("[yellow]DC[/yellow] - Después de la Conquista")
    console.print("[yellow]AC[/yellow] - Antes de la Conquista")
    era = Prompt.ask("Seleccione la era historica en que ocurrirá el evento:", choices=["DC", "AC"])

    console.print("\n[bold cyan]Recursos dsiponibles:[/bold cyan]")
    for resource_id, resource_data in RESOURCES.items():
        type = resource_data.resource_type if resource_data.resource_type is not None else "sin tipo"
        house = resource_data.house if resource_data.house is not None else "sin casa"
        console.print(f"{resource_id}: {resource_data.name} (tipo: {type}, casa: {house})")
    
    while True:
        resources_input = Prompt.ask("\nIngrese los ids de los recursos que desea agregar (separados por comas)")
        resources_ids = []
        ids_invalidos = []

        if not resources_input.strip():
            console.print("[yellow]No ingresó ningún recurso. Debe seleccionar al menos uno[/yellow]")
            continue

        try:
            separated_ids = resources_input.split(",")
            for id in separated_ids:
                if id.strip():
                    rid = int(id.strip())
                    if rid in RESOURCES:
                        resources_ids.append(rid)
                    else:
                        ids_invalidos.append(str(rid))
        except ValueError:
            console.print("[red]ids inválidos (deben ser números y estar separados por coma)[/red]")
            continue

        if ids_invalidos:
            ids_str = ''
            for i, id_invalido in enumerate(ids_invalidos):
                if i == 0:
                    ids_str = id_invalido
                else:
                    ids_str = ids_str + ", " + id_invalido
            
            console.print(f"[red]Error: Los siguientes ids no existen: {ids_str}[/red]")
            console.print("[yellow]Por favor, revise la lista de recursos disponibles e intente nuevamente[/yellow]")
            continue

        if not resources_ids:
            console.print("[yellow]Debe seleccionar al menos un recurso valido[/yellow]")
            continue
        
        break
    
    def ask_datetime(prompt_text):
        while True:
            try:
                year = int(Prompt.ask(f"\nAño - {prompt_text}"))
                month = int(Prompt.ask(f"Mes - {prompt_text} [1-12]"))
                day = int(Prompt.ask(f"Día - {prompt_text}"))
                hour = int(Prompt.ask(f"Hora - {prompt_text} [0-23]"))
                minute = int(Prompt.ask(f"Minuto - {prompt_text} [0-59]"))
                return datetime(year, month, day, hour, minute)
            except ValueError:
                console.print("[red]ups! error en la fecha. Inténtelo de nuevo[/red]")
            
    start_date = ask_datetime("Inicio")
    end_date = ask_datetime("Fin")
    if end_date <= start_date:
        console.print("[red]La fecha final debe ser posterior a la inicial[/red]")
        return
        
    if Confirm.ask("\nDesea buscar el próximo hueco disponible para estos recursos?"):
        duration_hours = (end_date - start_date).total_seconds() / 3600.0
        max_days = max(30, int(duration_hours / 24) + 10)

        console.print(f"[cyan]Buscando hueco en los próximos {max_days} días...[/cyan]")

        slot_start, slot_end = find_next_available_time_slot(resources_ids=resources_ids, duration_hours=duration_hours, start_from=start_date, max_days=max_days, existing_events=list_events(), resources=RESOURCES, restrictions=RESTRICTIONS, event_type=event_type)
        if slot_start and slot_end:
            console.print(f"[green]Hueco encontrado: {slot_start} - {slot_end}[/green]")
            if Confirm.ask("Desea usar este hueco?"):
                start_date, end_date = slot_start, slot_end
            else:
                return
        else:
            console.print("[red]No se encontró un hueco disponible en los próximos días sin conflicto de recursos o restricciones[/red]")
            return

    valid, result = add_event(name=name, description=desc, start=start_date, end=end_date, event_type=event_type, location=location, resources_ids=resources_ids, era=era)
    if valid:
        console.print(f"[green]Evento '{name}' agregado con ID: {result}[/green]")
    else:
        console.print(f"[red]{result}[/red]")
