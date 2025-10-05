# basado en el calendario ponienti
import re
def date_validation():
    fecha_str = []

    # 1. Validar patrón con regex
    if not re.match(r'^\d{1,3}-\d{1,2}-\d{1,2}$', fecha_str):
        return False, "Formato: AÑO-MES-DÍA (ej: 298-3-15)"
    
    try:
        partes = fecha_str.split('-')
        año = int(partes[0])
        mes = int(partes[1])
        dia = int(partes[2])
        
        # 2. Validar año (1-400 DC)
        if año < 1 or año > 400:
            return False, f"Año debe ser 1-400 DC"
        
        # 3. Validar mes
        if mes < 1 or mes > 12:
            return False, "Mes debe ser 1-12"
        
        # 4. Validar día según mes
        if mes in [1, 3, 5, 7, 8, 10, 12]:
            max_dias = 31
        elif mes in [4, 6, 9, 11]:
            max_dias = 30
        else:  # mes 2
            max_dias = 28  # Sin años bisiestos en Westeros
        
        if dia < 1 or dia > max_dias:
            return False, f"El mes {mes} tiene máximo {max_dias} días"
        
        return True, f"Fecha válida: {dia}/{mes}/{año} DC"
        
    except ValueError:
        return False, "La fecha debe contener solo números"
        