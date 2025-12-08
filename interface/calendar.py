from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime, timedelta
import calendar
from typing import List, Optional
from models.event import Event

console = Console()

def mostrar_calendario_mensual(ano: int, mes: int, eventos: List[Evento] = None) -> None:
    """
    Muestra un calendario mensual con los eventos marcados
    """
    if eventos is None:
        eventos = []
    
    # Obtener el calendario del mes
    cal = calendar.monthcalendar(ano, mes)
    nombre_mes = calendar.month_name[mes]
    
    # Crear tabla del calendario
    tabla = Table(
        title=f"🗓️ {nombre_mes.upper()} {ano} - CALENDARIO DE BATALLAS",
        show_header=True,
        header_style="bold magenta",
        style="white"
    )
    
    # Encabezados de días de la semana
    dias_semana = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
    for dia in dias_semana:
        tabla.add_column(dia, justify="center", style="cyan", width=12)
    
    # Procesar cada semana del mes
    for semana in cal:
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append("")  # Días vacíos (fuera del mes)
            else:
                celda = _formatear_dia(dia, ano, mes, eventos)
                fila.append(celda)
        tabla.add_row(*fila)
    
    # Mostrar el calendario
    console.print(tabla)
    
    # Mostrar leyenda y eventos del mes
    _mostrar_leyenda()
    _mostrar_eventos_mes(ano, mes, eventos)

def _formatear_dia(dia: int, ano: int, mes: int, eventos: List[Evento]) -> str:
    """
    Formatea un día del calendario marcando eventos activos
    """
    fecha_actual = datetime(ano, mes, dia)
    hoy = datetime.now().date()
    
    # Verificar si es hoy
    es_hoy = fecha_actual.date() == hoy
    
    # Buscar eventos para este día
    evento_activo = None
    for evento in eventos:
        if evento.inicio.date() <= fecha_actual.date() <= evento.fin.date():
            evento_activo = evento
            break
    
    if evento_activo:
        # Determinar el tipo de día en el evento
        if fecha_actual.date() == evento_activo.inicio.date():
            return f"[bold green]{dia} 🚀[/bold green]"  # Inicio
        elif fecha_actual.date() == evento_activo.fin.date():
            return f"[bold red]{dia} 🏁[/bold red]"      # Fin
        else:
            return f"[bold yellow]{dia} ⚔️[/bold yellow]"  # Durante
    elif es_hoy:
        return f"[bold blue]{dia} 📌[/bold blue]"  # Hoy sin eventos
    else:
        return str(dia)  # Día normal

def _mostrar_leyenda() -> None:
    """
    Muestra la leyenda de símbolos del calendario
    """
    console.print("\n[bold]🎯 LEYENDA DEL CALENDARIO:[/bold]")
    console.print("  [bold green]🚀[/bold green] Inicio de batalla")
    console.print("  [bold yellow]⚔️[/bold yellow] Batalla en curso")
    console.print("  [bold red]🏁[/bold red] Fin de batalla")
    console.print("  [bold blue]📌[/bold blue] Hoy")

def _mostrar_eventos_mes(ano: int, mes: int, eventos: List[Evento]) -> None:
    """
    Muestra la lista de eventos para el mes
    """
    eventos_mes = [e for e in eventos if e.inicio.month == mes and e.inicio.year == ano]
    
    if eventos_mes:
        console.print(f"\n[bold]📋 BATALLAS PROGRAMADAS PARA {calendar.month_name[mes].upper()}:[/bold]")
        for evento in eventos_mes:
            duracion = (evento.fin - evento.inicio).days + 1
            console.print(f"  • {evento.nombre}")
            console.print(f"    📅 {evento.inicio.strftime('%d/%m')} → {evento.fin.strftime('%d/%m')} ({duracion} días)")
            if evento.descripcion:
                console.print(f"    📝 {evento.descripcion}")
    else:
        console.print(f"\n[yellow]📝 No hay batallas programadas para {calendar.month_name[mes]}[/yellow]")

def mostrar_calendario_semanal(fecha_inicio: datetime, eventos: List[Evento] = None) -> None:
    """
    Muestra una vista semanal detallada con eventos
    """
    if eventos is None:
        eventos = []
    
    tabla = Table(
        title=f"📅 SEMANA DEL {fecha_inicio.strftime('%d/%m/%Y')}",
        show_header=True,
        header_style="bold blue"
    )
    
    tabla.add_column("Día", style="cyan", width=12)
    tabla.add_column("Fecha", style="magenta", width=10)
    tabla.add_column("Eventos", style="white")
    
    # Generar la semana (7 días a partir de fecha_inicio)
    for i in range(7):
        fecha = fecha_inicio + timedelta(days=i)
        dia_nombre = fecha.strftime("%A")
        fecha_str = fecha.strftime("%d/%m")
        
        # Buscar eventos para este día
        eventos_dia = [e for e in eventos if e.inicio.date() <= fecha.date() <= e.fin.date()]
        
        if eventos_dia:
            eventos_texto = "\n".join([f"⚔️ {e.nombre} ({e.inicio.strftime('%H:%M')}-{e.fin.strftime('%H:%M')})" 
                                      for e in eventos_dia])
            estilo = "bold red"
            tabla.add_row(dia_nombre, fecha_str, eventos_texto, style=estilo)
        else:
            tabla.add_row(dia_nombre, fecha_str, "📝 Sin eventos")
    
    console.print(tabla)

def mostrar_vista_rapida(eventos: List[Evento]) -> None:
    """
    Muestra una vista rápida de los próximos eventos
    """
    hoy = datetime.now().date()
    eventos_futuros = [e for e in eventos if e.inicio.date() >= hoy]
    eventos_futuros.sort(key=lambda x: x.inicio)
    
    if eventos_futuros:
        console.print(Panel("⚡ PRÓXIMAS BATALLAS", style="bold red"))
        
        for evento in eventos_futuros[:5]:  # Mostrar solo los 5 próximos
            dias_faltantes = (evento.inicio.date() - hoy).days
            estado = "HOY" if dias_faltantes == 0 else f"en {dias_faltantes} días"
            
            console.print(f"  [bold]{evento.nombre}[/bold]")
            console.print(f"    📅 {evento.inicio.strftime('%d/%m/%Y')} ({estado})")
            console.print(f"    ⏱️  {evento.inicio.strftime('%H:%M')} - {evento.fin.strftime('%H:%M')}")
            
            if evento.recursos_ids:
                console.print(f"    🎯 Recursos: {', '.join(evento.recursos_ids[:3])}" + 
                             ("..." if len(evento.recursos_ids) > 3 else ""))
            console.print("")  # Línea en blanco
        
        if len(eventos_futuros) > 5:
            console.print(f"📖 ... y {len(eventos_futuros) - 5} batallas más")
    else:
        console.print(Panel("📝 No hay batallas programadas", style="yellow"))

def mostrar_resumen_mensual(eventos: List[Evento]) -> None:
    """
    Muestra un resumen de eventos por mes
    """
    # Agrupar eventos por mes
    eventos_por_mes = {}
    for evento in eventos:
        clave = (evento.inicio.year, evento.inicio.month)
        if clave not in eventos_por_mes:
            eventos_por_mes[clave] = []
        eventos_por_mes[clave].append(evento)
    
    if eventos_por_mes:
        console.print(Panel("📊 RESUMEN MENSUAL DE BATALLAS", style="bold green"))
        
        for (ano, mes), eventos_mes in sorted(eventos_por_mes.items()):
            nombre_mes = calendar.month_name[mes]
            console.print(f"  [bold]{nombre_mes} {ano}:[/bold] {len(eventos_mes)} batallas")
            
            for evento in eventos_mes:
                console.print(f"    • {evento.nombre} ({evento.inicio.strftime('%d/%m')})")
    
    else:
        console.print(Panel("📝 No hay batallas programadas", style="yellow"))

# Función principal para interfaz de calendario
def menu_calendario(eventos: List[Evento]) -> None:
    """
    Menú interactivo del sistema de calendarios
    """
    while True:
        console.print(Panel(Text("🗓️ SISTEMA DE CALENDARIOS BÉLICOS", justify="center"), style="bold red"))
        
        opciones = """
    [1] 📅 Ver calendario mensual
    [2] 📋 Ver semana actual
    [3] ⚡ Próximas batallas
    [4] 📊 Resumen mensual
    [5] 🏰 Volver al menú principal
        """
        console.print(opciones)
        
        try:
            from rich.prompt import IntPrompt
            opcion = IntPrompt.ask("Selecciona una opción", choices=["1", "2", "3", "4", "5"])
            
            if opcion == 1:
                _menu_calendario_mensual(eventos)
            elif opcion == 2:
                fecha_lunes = datetime.now() - timedelta(days=datetime.now().weekday())
                mostrar_calendario_semanal(fecha_lunes, eventos)
            elif opcion == 3:
                mostrar_vista_rapida(eventos)
            elif opcion == 4:
                mostrar_resumen_mensual(eventos)
            elif opcion == 5:
                console.print("[yellow]🏰 Volviendo al menú principal...[/yellow]")
                break
            
            if opcion != 5:
                input("\nPresiona Enter para continuar...")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]⚡ Operación cancelada[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")

def _menu_calendario_mensual(eventos: List[Evento]) -> None:
    """
    Submenú para seleccionar mes y año del calendario
    """
    from rich.prompt import IntPrompt
    
    console.print(Panel("📅 CALENDARIO MENSUAL", style="blue"))
    
    # Capturar año y mes
    ano_actual = datetime.now().year
    mes_actual = datetime.now().month
    
    ano = IntPrompt.ask("Ingresa el año", default=ano_actual, show_default=True)
    mes = IntPrompt.ask("Ingresa el mes (1-12)", default=mes_actual, show_default=True)
    
    if 1 <= mes <= 12:
        mostrar_calendario_mensual(ano, mes, eventos)
    else:
        console.print("[red]❌ Error: El mes debe estar entre 1 y 12[/red]")

# Función de utilidad para otros módulos
def obtener_fecha_actual() -> datetime:
    """Retorna la fecha y hora actual"""
    return datetime.now()

def formatear_fecha(fecha: datetime) -> str:
    """Formatea una fecha para mostrar"""
    return fecha.strftime("%d/%m/%Y %H:%M")