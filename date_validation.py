# import datetime
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
    esta funcion devuelve true si se solapan los intervalos de tiempo y False en caso contrario
    '''
    if intervalo_1[0] < intervalo_2[1] and intervalo_1[0] >= intervalo_2[0]:
        return True
    if intervalo_2[0] >= intervalo_1[0] and intervalo_2[0] < intervalo_1[1]:
        return True
    return False