from rich.table import Table
from rich.console import Console


def command_list_planned_events():
    console = Console()
    table = Table(title="Lista de Eventos") 
    table.add_column("ID", style="cyan") 
    table.add_column("Descripción", style="magenta") 
    table.add_column("Estado", style="green")

    for id, event in events.items(): 
        table.add_row(str(id), event['desc'], event['estado'])

    console.print(table)
    #!agregar mas info de los eventos a la tabla

#!usar estas tablas para listar el inventario de recursos y eventos y demas
# tabla = Table(title="Ejércitos de Poniente")
# tabla.add_column("Casa", style="cyan")
# tabla.add_column("Líder", style="magenta")
# tabla.add_column("Tropas", justify="right")
# tabla.add_row("Stark", "Robb Stark", "20,000")
# tabla.add_row("Lannister", "Tywin Lannister", "35,000")
# console.print(tabla)