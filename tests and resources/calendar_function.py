from rich.console import Console
from rich.table import Table
import calendar

console = Console()


def show_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    tabla = Table(title=f"{month_name} {year}", show_header=True, header_style="bold magenta")
 
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    for dia in dias_semana:
        tabla.add_column(dia, justify="center", style="cyan")
    
    for semana in cal:
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append("")  # Días vacíos
            else:
                fila.append(str(dia))
        tabla.add_row(*fila)
    
    console.print(tabla)


show_calendar(2025, 2)
