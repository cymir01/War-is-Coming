from rich.console import Console
from src.services.data_manager import list_events, delete_event

def command_delete_event():
    console = Console()
    events = list_events()
    if not events:
        console.print("[yellow]No hay eventos para eliminar[/yellow]")
        return
    
    console.print("[bold cyan]Eventos existentes:[/bold cyan]")
    for event in events:
        console.print(f"id: {event.id} - {event.name} ({event.start.strftime('%Y-%m-%d %H:%M')})")
    
    while True:
        cmd = console.input("Introduzca el id del evento que desea eliminar o presione 's' para salir:")
        if cmd.lower() == 's':
            break
        try:
            event_id = int(cmd)
        except ValueError:
            console.print("[red]id invalido (debe ser un numero)[/red]")
            continue
        if delete_event(event_id):
            console.print(f"[green]Evento {event_id} eliminado satisfactoriamente :)[/green]")
        else:
            console.print(f"[red]No se encontro ningun evento con id {event_id}[/red]")
        
        break