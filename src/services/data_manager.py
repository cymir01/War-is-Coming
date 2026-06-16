import json 
import os
from src.models.event import Event

FILEPATH = "src/services/war_planner.json"
EVENTS = {}
RESOURCES = {}
NEXT_EVENT_ID = 1

def load_data():
    global EVENTS, RESOURCES, NEXT_EVENT_ID

    if not os.path.exists(FILEPATH):
        return None

    try:
        with open(FILEPATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

            events_dict = data.get('events', {})
            EVENTS = {}
            for event_id, event_data in events_dict.items():
                EVENTS[int(event_id)] = Event.from_dict(event_data)

            RESOURCES = data.get('resources', {})
            NEXT_EVENT_ID = data.get('next_event_id', 1)

            EVENTS = {int(k): v for k, v in EVENTS.items()}

    except Exception as e:
        print(f"Error al cargar datos: {e}")

def save_data():
    global EVENTS, RESOURCES, NEXT_EVENT_ID

    data = {
        'events': EVENTS,
        'next_event_id': NEXT_EVENT_ID,
    }
    
    with open(FILEPATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_event(name, description, start, end, era, status=None, resources_ids=None):
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

    EVENTS[NEXT_EVENT_ID] = event.to_dict()
    print(f"Evento '{name}' agregado (ID: {NEXT_EVENT_ID})\n")
    NEXT_EVENT_ID += 1
    save_data()

    #agregar por aqui la llamada a la funcion que verficia si hay overlapping entre eventos, pero tambien tengo que 
    #que verificar si hay conflicto 

def list_events():
    return EVENTS.copy()

load_data()

print(list_events())