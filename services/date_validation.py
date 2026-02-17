from datetime import datetime

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
            if not (1 <= year <= 302):
                return False, "Año DC fuera de rango histórico (1-302 DC)", None
        else:
            return False, f"Era desconocida: '{era}'. Use 'AC' o 'DC'", None
    
        dt = datetime(year, month, day, hours, minutes)
        return True, "", dt

    except ValueError as e:
        return False, f"[red]Error de fecha: {str(e)}. Intente de nuevo[/red]", None

#!invetigar por que overlap como lo escribi no cubre todos los casos
def overlap(intervalo_1, intervalo_2): #intervalos son listas con dos elementos (fecha inicio y de fin)
    '''
    esta funcion devuelve True si se solapan los intervalos de tiempo y False en caso contrario
    '''
    inicio1, fin1 = intervalo_1
    inicio2, fin2 = intervalo_2
    return max(inicio1, inicio2) < min(fin1, fin2)
'''
if intervalo_2[1] > intervalo_1[0] >= intervalo_2[0]:
        return True
    if intervalo_1[1] > intervalo_2[0] >= intervalo_1[0]:
        return True
    return False
'''

def is_new_event_overlapping_existing(new_event, existing_events): 
    """debe tener por parametros una lista con fecha de inicio y
    fin del evemto ingresado y otra lista de listas con 
    los intervalos de los evemtos existentes"""
    for event in existing_events:
        if overlap(new_event, event):
            return True
    return False

# fecha = datetime(2000, 2, 10, 12, 00, 00)
# otra = datetime(2000, 10, 10, 12, 30, 00)
# fecha1 = datetime(100, 4, 2)
# fecha2 = datetime(400, 3, 4)
# fecha3 = datetime(2000, 11, 1, 12, 00, 00)
# fecha4 = datetime(2010, 5, 10, 12, 00, 00)

# print(is_new_event_overlapping_existing([fecha, otra], [[fecha1, fecha2], [fecha3, fecha4]]))

# year_s = Prompt.ask("Año") 
# era = Prompt.ask("era") 
# day = Prompt.ask("dia") 
# month = Prompt.ask("mes") 
# hours = Prompt.ask("horas")
# minutes = Prompt.ask("minutos")

# ok, msg, start = validate_datetime_input(year_s, month, day, hours, minutes, era) 