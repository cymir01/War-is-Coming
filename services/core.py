import json 
import os
from models.event import Event

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

def add_event(name, description, start, end, era, status=None, resources_ids=None): #instanciar la clase Event aqui
    global NEXT_EVENT_ID
    from datetime import datetime
    #asegurar que start y end sean objetos datetime

    event = Event(
        start=start,
        end=end,
        name=name,
        era=era,
        status=status,
        resources=resources_ids or [],
        description=description
    )
    
    #event.to_dict()... no debe ir aqui fuera debe guardarse en EVENTS como 
    # ocurre en la linea 59, si no el programa lanza:
    # TypeError: Object of type Event is not JSON serializable porque intenta
    #guardar una instancia de clase en lugar de un 

    EVENTS[NEXT_EVENT_ID] = event.to_dict() 
    print(f"Evento '{name}' agregado (ID: {NEXT_EVENT_ID})\n")
    NEXT_EVENT_ID += 1
    save_data()

def list_events():
    return EVENTS.copy()

def list_resources():
    return RESOURCES.copy()

load_data()

print(list_events())