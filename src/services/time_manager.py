from datetime import datetime, timedelta


def overlap(interval_1, interval_2): #intervalos son listas con dos elementos (fecha inicio y de fin)
    '''
    esta funcion devuelve True si se solapan los intervalos de tiempo y False en caso contrario
    '''
    start1, end1 = interval_1
    start2, end2 = interval_2
    return max(start1, start2) < min(end1, end2)


def is_new_event_overlapping_existing(new_event, existing_events):
    """debe tener por parametros una lista con fecha de inicio y
    fin del evemto ingresado y otra lista de listas con 
    los intervalos de los evemtos existentes"""
    for event in existing_events:
        if overlap(new_event, event):
            return True
    return False

# Debes implementar una función inteligente que, dado un evento y los recursos que necesita, sea capaz de analizar el calendario y 
# sugerir el próximo intervalo de tiempo disponible donde se pueda realizar sin conflictos ni violaciones de restricciones.
def find_next_available_time_slot(resource_ids, duration_hours, start_from=None, max_days=30):
    from services.data_manager import EVENTS, RESOURCES

    for rid in resource_ids:
        if rid not in RESOURCES:

            return False, None, f"El recurso {rid} no existe"
    if duration_hours <= 0:
        return False, None, "La duración debe ser positiva"