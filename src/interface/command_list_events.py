from rich.table import Table
from rich.console import Console
from src.services.data_manager import list_events


def command_list_planned_events():
    console = Console()
    events = list_events()
    if not events:
        console.print("[yellow]No hay eventos programados[/yellow]")
        return
    
    table = Table(title="Lista de Eventos") 
    table.add_column("ID", style="cyan")
    table.add_column("Nombre", style="white")
    table.add_column("Tipo", style="magenta")
    table.add_column("Descripción", style="magenta")
    table.add_column("Estado", style="magenta") 
    table.add_column("Inicio", style="green")
    table.add_column("Fin", style="green")
    table.add_column("Recursos", style="yellow")

#este bloque convierte la lista de ids en una cadena de texto porque la funcion table.add_row() espera cadenas de texto
    for event in events:
        resources_str = ""
        for i, rid in enumerate(event.resources_ids):
            if i == 0:
                resources_str = str(rid)
            else:
                resources_str = resources_str + ", " + str(rid)

        table.add_row(
            str(event.id),
            event.name,
            event.event_type,
            event.description,
            event.status,
            event.start.strftime("%Y-%m-%d %H:%M"),
            event.end.strftime("%Y-%m-%d %H:%M"),
            resources_str
        )

    console.print(table)