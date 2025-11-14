import json 
import os
FILEPATH = "tasks.json"
TAREAS = {}
NEXT_ID = 1


def guardar_tareas():
    global TAREAS, NEXT_ID
    data = {
    'tareas': TAREAS,
    'next_id': NEXT_ID
    }
    with open(FILEPATH, 'w') as f:
        json.dump(data, f, indent=4)


def cargar_tareas():
    global TAREAS, NEXT_ID

    if not os.path.exists(FILEPATH):
        return  # No hay datos que cargar

    try:
        with open(FILEPATH, 'r') as f:
            data = json.load(f)
            TAREAS = data.get('tareas', {})
            NEXT_ID = data.get('next_id', 1) # Convertir claves de JSON (string) a int
            TAREAS = {int(k): v for k, v in TAREAS.items()} 
    except Exception as e: 
        print(f"Error al cargar datos: {e}")


def agregar_tarea(descripcion):
    global NEXT_ID  
    TAREAS[NEXT_ID] = {'desc': descripcion, 'estado': 'pendiente'} 
    print(f"Tarea {NEXT_ID} agregada.\n") 
    NEXT_ID += 1
    guardar_tareas()


def listar_tareas():
    return TAREAS.copy()


cargar_tareas()
