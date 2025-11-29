import json 
import os
FILEPATH = "war_planner.json"
EVENTS = {}
RESOURCES = {}
NEXT_EVENT_ID = 1
NEXT_RESOURCE_ID = 1

def save_data():
    global EVENTS, RESOURCES, NEXT_EVENT_ID, NEXT_RESOURCE_ID
    data = {
    'events': EVENTS,
    'resources': RESOURCES,
    'next_event_id': NEXT_EVENT_ID,
    'next_resource_id': NEXT_RESOURCE_ID
    }
    with open(FILEPATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_data():
    global EVENTS, RESOURCES, NEXT_EVENT_ID, NEXT_RESOURCE_ID

    if not os.path.exists(FILEPATH):
        return

    try:
        with open(FILEPATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            EVENTS = data.get('events', {})
            RESOURCES = data.get('resources', {})
            NEXT_EVENT_ID = data.get('next_event_id', 1)
            NEXT_RESOURCE_ID = data.get('next_resource_id', 1)
            
            EVENTS = {int(k): v for k, v in EVENTS.items()}
            RESOURCES = {int(k): v for k, v in RESOURCES.items()}
            
    except Exception as e:
        print(f"Error al cargar datos: {e}")


def agregar_tarea(descripcion):
    global NEXT_ID  
    TAREAS[NEXT_ID] = {'desc': descripcion, 'estado': 'pendiente'} 
    print(f"Tarea {NEXT_ID} agregada.\n") 
    NEXT_ID += 1

def add_event(name, start, end, resources_ids=None):
    global NEXT_EVENT_ID
    from datetime import datetime
    
    event = {
        'id': NEXT_EVENT_ID,
        'name': name,
        'start': start.isoformat() if isinstance(start, datetime) else start,
        'end': end.isoformat() if isinstance(end, datetime) else end,
        'resources_ids': resources_ids or [],
        'estado': 'planificado',
        'tipo': 'batalla'
    }
    
    EVENTS[NEXT_EVENT_ID] = event
    print(f"Evento '{name}' agregado (ID: {NEXT_EVENT_ID})\n")
    NEXT_EVENT_ID += 1
    save_data()
    return event

def list_events():
    return EVENTS.copy()

def list_available_resources():
    pass

load_data()
