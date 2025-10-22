day = int(input("Día: "))
month = int(input("Mes: "))
year = int(input("Año: "))

valid = False

if month == 2:
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        # Note que aquí igualamos contra la condición directamente
        valid = day > 0 and day <= 29
    else:
        valid = day > 0 and day <= 28
else:
    if month <= 7:
        # Aquí está el truco de la fórmula con el módulo
        #
        # Si el mes es par month%2 da 0 -> 30+0=30 debería tener
        # 30 días
        #
        # Si el mes es impar month%2 da 1 -> 30+1=31 debería
        # tener 31 días
        if day <= 30 + month % 2 and day > 0:
            valid = True
    elif month <= 12:
        # Aquí de usamos también el truco pero los valores se
        # invierten, por eso empezamos en 31 y restamos
        #
        # Si el mes es par month%2 da 0 -> 31-0=31 debería tener
        # 31 días
        #
        # Si el mes es impar month%2 da 1 -> 31-1=30 debería tener
        # 30 días
        if day <= 31 - (month % 2) and day > 0:
            valid = True

# Aquí sintaxis extra. Además del if-else como instrucción con
# bloques de código asociados, existe una expresión if.
#
# boolean_expression if condition else boolean_expression
#
# Esta expresión da como resultado el valor de la izquierda si la
# condición da True, sino, da como resultado el valor de la
# derecha
print(f"La fecha {"" if valid else "no "}es válida")
