from datetime import datetime, timedelta

# Debes implementar una función inteligente que, dado un evento y los recursos que necesita, sea capaz de analizar el calendario y 
# sugerir el próximo intervalo de tiempo disponible donde se pueda realizar sin conflictos ni violaciones de restricciones.
def find_next_available_time_slot(resource_ids, duration_hours, start_from=None, max_days=30):
    from core import EVENTS, RESOURCES

    for rid in resource_ids:
        if rid not in RESOURCES:
            return False, None, f"Recurso {rid} no existe"
    if duration_hours <= 0:
        return False, None, "Duración debe ser positiva"
    

    
    