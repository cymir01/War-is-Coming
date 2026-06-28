from rich.console import Console
from rich.table import Table
from src.services.data_manager import get_event_by_id, get_event_by_resource, RESOURCES

def command_view_details():
    console = Console()
    while True:
        console.print("\n[bold cyan]Ver detalles[/bold cyan]")
        console.print("Seleccione una accion:")
        console.print("  [yellow]e[/yellow] - ver detalles de un evento")
        console.print("  [yellow]r[/yellow] - ver agenda de un recurso")
        console.print("  [yellow]s[/yellow] - salir")
        
        action = console.input("\nAcción: ").strip().upper()

        if action == 'S':
            break

        if action == 'E':
            cmd = console.input("Introduzca el ID del evento para mostrar los detalles: ")
            try:
                event_id = int(cmd)
            except ValueError:
                console.print("[red]id inválido (debe ser un número)[/red]")
                continue

            event = get_event_by_id(event_id)
            if not event:
                console.print("[red]El evento no existe![/red]")
                continue

            table = Table(title=f"Detalles del evento número {event.id}")
            table.add_column("Campo", style="cyan")
            table.add_column("Valor", style="white")

            resources_str = ""
            for i, rid in enumerate(event.resources_ids):
                if i == 0:
                    resources_str = str(rid)
                else:
                    resources_str = resources_str + ", " + str(rid)

            table.add_row("Nombre", event.name)
            table.add_row("Descripción", event.description or "sin descripción")
            table.add_row("Tipo", event.event_type)
            table.add_row("Era", event.era)
            table.add_row("Ubicación", event.location or "no especificada")
            table.add_row("Inicio", event.start.strftime("%Y-%m-%d %H:%M"))
            table.add_row("Fin", event.end.strftime("%Y-%m-%d %H:%M"))
            table.add_row("Duración", str(event.get_duration()))
            table.add_row("Recursos", resources_str)
            table.add_row("Estado", event.status)
            
            console.print(table)
        
        elif action == 'R':
            cmd = console.input("Introduzca el id del recurso: ")
            try:
                resource_id = int(cmd)
            except ValueError:
                console.print("[red]id inválido.. debe ser un numero[/red]")
                continue
            
            if resource_id not in RESOURCES:
                console.print("[red]El recurso no existe[/red]")
                continue
            
            resource = RESOURCES[resource_id]
            events = get_event_by_resource(resource_id)
            
            if not events:
                console.print(f"[yellow]El recurso '{resource.name}' no esta asignado a ningun evento[/yellow]")
                continue
            
            table = Table(title=f"Agenda del recurso: {resource.name} (ID: {resource.id})")
            table.add_column("Evento ID", style="cyan")
            table.add_column("Nombre", style="white")
            table.add_column("Tipo", style="magenta")
            table.add_column("Era", style="yellow")
            table.add_column("Inicio", style="green")
            table.add_column("Fin", style="green")
            table.add_column("Estado", style="yellow")
            
            for event in events:
                table.add_row(
                    str(event.id),
                    event.name,
                    event.event_type,
                    event.era,
                    event.start.strftime("%Y-%m-%d %H:%M"),
                    event.end.strftime("%Y-%m-%d %H:%M"),
                    event.status
                )
            
            console.print(table)
        else:
            console.print("Acción inválida. Elija E, R o S..[/red]")