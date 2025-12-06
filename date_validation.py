from datetime import datetime

def valid_year_westeros(year, era): 
    #!me di cuenta de que tiene que validar el año segun si es AC o DC
    #!AC hay 6000 años y DC hay 302
    """Valida años según la era historica del calendario ponienti, a partir
    de la llegada de los Ándalos en adelante"""
    if era == "AC": #!poner prints explicando los errores
        return 1 <= year <= 6000
    elif era == "DC":
        return 1 <= year <= 302
    return False

def overlap(intervalo_1, intervalo_2): #intervalos son listas con dos elementos (fecha inicio y de fin)
    '''
    esta funcion devuelve True si se solapan los intervalos de tiempo y False en caso contrario
    '''
    if intervalo_2[1] > intervalo_1[0] >= intervalo_2[0]:
        return True
    if intervalo_1[1] > intervalo_2[0] >= intervalo_1[0]:
        return True
    return False
'''otra via:
def overlap(intervalo_1, intervalo_2):
    inicio1, fin1 = intervalo_1
    inicio2, fin2 = intervalo_2
    return max(inicio1, inicio2) < min(fin1, fin2)
'''

def is_new_event_overlapping_existing(new_event, existing_events): 
    """debe tener por parametros una lista con fecha de inicio y
    fin del evemto ingresado y otra lista de listas con 
    los intervalos de los evemtos existentes"""
    for event in existing_events:
        if overlap(new_event, event):
            return True
    return False

fecha = datetime(2000, 2, 10, 12, 00, 00)
otra = datetime(2000, 10, 10, 12, 30, 00)
fecha1 = datetime(100, 4, 2)
fecha2 = datetime(400, 3, 4)
fecha3 = datetime(2000, 11, 1, 12, 00, 00)
fecha4 = datetime(2010, 5, 10, 12, 00, 00)

# print(is_new_event_overlapping_existing([fecha, otra], [[fecha1, fecha2], [fecha3, fecha4]]))


def find_available_time_slot():
    pass

