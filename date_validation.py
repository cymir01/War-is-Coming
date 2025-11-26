from datetime import datetime
def valid_date(year, month, day):
    valid = False

    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            valid = day > 0 and day <= 29
        else:
            valid = day > 0 and day <= 28
    else:
        if month <= 7:
            if day <= 30 + month % 2 and day > 0:
                valid = True
        elif month <= 12:
            if day <= 31 - (month % 2) and day > 0:
                valid = True
    return valid

# print(valid_date(2004, 2, 29))

def overlap(intervalo_1, intervalo_2): #intervalos son listas con dos elementos (fecha inicio y de fin)
    '''
    esta funcion devuelve True si se solapan los intervalos de tiempo y False en caso contrario
    '''
    if intervalo_2[1] > intervalo_1[0] >= intervalo_2[0]:
        return True
    if intervalo_1[1] > intervalo_2[0] >= intervalo_1[0]:
        return True
    return False
'''Codigo generado por DeepSeek para overlap (basicamente hace lo mismo):
def overlap(intervalo_1, intervalo_2):
    inicio1, fin1 = intervalo_1
    inicio2, fin2 = intervalo_2
    return max(inicio1, inicio2) < min(fin1, fin2)
'''

def is_new_event_overlapping_existing(new_event, existing_events): #debe tener por parametros una lista con fecha de inicio y fin del evemto ingresado y otra lista de listas con los intervalos de los evemtos existentes
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

print(is_new_event_overlapping_existing([fecha, otra], [[fecha1, fecha2], [fecha3, fecha4]]))

