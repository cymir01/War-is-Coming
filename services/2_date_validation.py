from datetime import datetime, timedelta
from rich.prompt import Prompt

def validate_datetime_input(year, month, day, hours, minutes, era):
    """
    Valida una fecha completa según el calendario de Poniente.
    Incluye: rangos básicos + reglas históricas (AC/DC).
    """
    try:
        if not (1 <= month <= 12):
            return False, "Mes inválido. Debe estar entre 1 y 12", None
        if not (1 <= day <= 30):
            return False, "Día inválido. En Poniente todos los meses tienen 30 días", None
        if not (0 <= hours <= 23):
            return False, "Hora inválida. Debe estar entre 0 y 23", None
        if not (0 <= minutes <= 59):
            return False, "Minutos inválidos. Deben estar entre 0 y 59", None
        if year < 1:
            return False, "Año inválido. Debe ser ≥ 1", None

        if era == "AC":
            if not (1 <= year <= 6000):
                return False, "Año AC fuera de rango histórico (1-6000 AC)", None
        elif era == "DC":
            if not (1 <= year <= 302):  # ✅ CORRECTO: hasta 302 DC
                return False, "Año DC fuera de rango histórico (1-302 DC)", None
        else:
            return False, f"Era desconocida: '{era}'. Use 'AC' o 'DC'", None
    
        dt = datetime(year, month, day, hours, minutes)
        return True, "", dt

    except ValueError as e:
        return False, f"[red]Error de fecha: {str(e)}. Intente de nuevo[/red]", None


def overlap(intervalo_1, intervalo_2):
    """
    Comprueba si dos intervalos de tiempo se solapan.
    
    Args:
        intervalo_1: [datetime_inicio, datetime_fin]
        intervalo_2: [datetime_inicio, datetime_fin]
    
    Returns:
        bool: True si se solapan, False en caso contrario
        
    Ejemplo:
        intervalo_1 = [datetime(298, 1, 1), datetime(298, 1, 10)]
        intervalo_2 = [datetime(298, 1, 5), datetime(298, 1, 15)]
        overlap(intervalo_1, intervalo_2)  # True (se solapan del 5 al 10)
    """
    inicio1, fin1 = intervalo_1
    inicio2, fin2 = intervalo_2
    
    # Dos intervalos se solapan si: max(inicio) < min(fin)
    return max(inicio1, inicio2) < min(fin1, fin2)


def is_new_event_overlapping_existing(new_event, existing_events):
    """
    Comprueba si un evento nuevo choca con eventos existentes.
    
    Args:
        new_event: [datetime_inicio, datetime_fin] del nuevo evento
        existing_events: lista de [datetime_inicio, datetime_fin] de eventos existentes
    
    Returns:
        bool: True si hay conflicto, False si está disponible
        
    Ejemplo:
        nuevo = [datetime(298, 1, 5), datetime(298, 1, 15)]
        existentes = [
            [datetime(298, 1, 1), datetime(298, 1, 10)],
            [datetime(298, 2, 1), datetime(298, 2, 5)]
        ]
        is_new_event_overlapping_existing(nuevo, existentes)  # True
    """
    for event in existing_events:
        if overlap(new_event, event):
            return True
    return False


def find_available_time_slot(
    event_duration,
    required_resources,
    start_after=None,
    existing_events=None,
    available_resources=None,
    max_search_days=360
):
    
    # Valores por defecto
    if start_after is None:
        start_after = datetime(1, 1, 1, 0, 0)
    
    if existing_events is None:
        existing_events = []
    
    if available_resources is None:
        available_resources = {}
    
    # ════════════════════════════════════════════════════════════
    # VALIDACIÓN 1: Recursos disponibles
    # ════════════════════════════════════════════════════════════
    for resource_id in required_resources:
        if resource_id not in available_resources:
            print(f"Recurso {resource_id} no encontrado en inventario")
            return None
        if available_resources[resource_id] <= 0:
            print(f"❌ Recurso {resource_id} no está disponible (cantidad: {available_resources[resource_id]})")
            return None
    
    # ════════════════════════════════════════════════════════════
    # LÍMITES DEL CALENDARIO
    # ════════════════════════════════════════════════════════════
    # Máximo absoluto: último segundo del 302 DC
    absolute_max = datetime(302, 12, 30, 23, 59)
    
    # Rango de búsqueda: desde start_after hasta max_search_days adelante
    # pero nunca más allá del 302 DC
    max_end_date = start_after + timedelta(days=max_search_days)
    max_end_date = min(max_end_date, absolute_max)
    
    # ════════════════════════════════════════════════════════════
    # BÚSQUEDA: Iterar día a día
    # ════════════════════════════════════════════════════════════
    current_start = start_after
    
    while current_start < max_end_date:
        # Calcular el final del evento propuesto
        proposed_end = current_start + event_duration
        
        # Validar que no excede el límite máximo del calendario
        if proposed_end > absolute_max:
            print(f"No hay espacio disponible antes del fin del calendario (302-12-30)")
            return None
        
        # Crear el intervalo propuesto
        proposed_interval = [current_start, proposed_end]
        
        # Verificar si hay conflicto de tiempo
        if not is_new_event_overlapping_existing(proposed_interval, existing_events):
            #SLOT DISPONIBLE ENCONTRADO
            print(f"✅ Slot disponible encontrado:")
            print(f"   Inicio:  {current_start.year:03d}-{current_start.month:02d}-{current_start.day:02d} "
                  f"{current_start.hour:02d}:{current_start.minute:02d}")
            print(f"   Fin:     {proposed_end.year:03d}-{proposed_end.month:02d}-{proposed_end.day:02d} "
                  f"{proposed_end.hour:02d}:{proposed_end.minute:02d}")
            print(f"   Duración: {(proposed_end - current_start).days} días")
            return (current_start, proposed_end)
        
        # No disponible, avanzar al siguiente día
        current_start += timedelta(days=1)
    
    print(f"❌ No se encontró slot disponible en los próximos {max_search_days} días")
    return None


def find_available_time_slot_optimized(
    event_duration,
    required_resources,
    start_after=None,
    existing_events=None,
    available_resources=None,
    max_search_days=360
):
    """
    Versión OPTIMIZADA: Salta directamente al final de eventos que causan conflicto.
    
    Mucho más eficiente que la versión anterior cuando hay muchos eventos.
    Reduce el número de iteraciones significativamente.
    
    Los parámetros son idénticos a find_available_time_slot().
    
    Ejemplo:
        # En lugar de buscar día a día, salta sobre eventos conflictivos
        slot = find_available_time_slot_optimized(
            event_duration=timedelta(days=30),
            required_resources=[1, 2],
            start_after=datetime(298, 1, 1, 0, 0),
            existing_events=[
                [datetime(298, 1, 1), datetime(298, 1, 50)],
                [datetime(298, 2, 1), datetime(298, 2, 100)]
            ],
            available_resources={1: 500, 2: 100}
        )
    """
    
    if start_after is None:
        start_after = datetime(1, 1, 1, 0, 0)
    
    if existing_events is None:
        existing_events = []
    
    if available_resources is None:
        available_resources = {}
    
    # Validar recursos
    for resource_id in required_resources:
        if resource_id not in available_resources or available_resources[resource_id] <= 0:
            return None
    
    current_start = start_after
    max_end_date = start_after + timedelta(days=max_search_days)
    absolute_max = datetime(302, 12, 30, 23, 59)
    max_end_date = min(max_end_date, absolute_max)
    
    iterations = 0
    
    while current_start < max_end_date:
        iterations += 1
        
        proposed_end = current_start + event_duration
        
        # Validar límite máximo
        if proposed_end > absolute_max:
            print(f"❌ No hay espacio disponible antes del 302-12-30")
            return None
        
        proposed_interval = [current_start, proposed_end]
        
        # Buscar conflictos
        conflict_found = False
        latest_conflict_end = None
        
        for existing_event in existing_events:
            if overlap(proposed_interval, existing_event):
                conflict_found = True
                # Guardar el fin del evento que causa conflicto (el más tarde)
                if latest_conflict_end is None or existing_event[1] > latest_conflict_end:
                    latest_conflict_end = existing_event[1]
        
        if not conflict_found:
            # ✅ SLOT DISPONIBLE
            print(f"✅ Slot encontrado en {iterations} iteraciones:")
            print(f"   Inicio:  {current_start.year:03d}-{current_start.month:02d}-{current_start.day:02d} "
                  f"{current_start.hour:02d}:{current_start.minute:02d}")
            print(f"   Fin:     {proposed_end.year:03d}-{proposed_end.month:02d}-{proposed_end.day:02d} "
                  f"{proposed_end.hour:02d}:{proposed_end.minute:02d}")
            print(f"   Duración: {(proposed_end - current_start).days} días")
            return (current_start, proposed_end)
        
        # ⚡ OPTIMIZACIÓN: Saltar al final del último evento conflictivo
        # En lugar de avanzar solo 1 día, saltamos directamente
        if latest_conflict_end:
            current_start = latest_conflict_end
        else:
            current_start += timedelta(days=1)
    
    print(f"No se encontró slot disponible")
    return None