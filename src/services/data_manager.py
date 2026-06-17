import json 
import os
from src.models.event import Event

FILEPATH = "src/services/war_planner.json"
EVENTS = [] #cambiar el codigo que gestiona events para que opere con lista y no dict
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

def events_binary_cronological_sort(events_list, new_event):
        if events_list == []:
            return [new_event]
    
        if new_event in events_list:
            print("El evento ya existe")
            return events_list
        
        left = 0
        right = len(events_list) - 1
        index = len(events_list)

        while left <= right:
            midle = (left + right)//2
            if new_event.get_start_date() < events_list[midle].get_start_date(): 
                index = midle
                right = midle - 1
            else:
                left = midle + 1
    
        if(index == len(events_list)):
            events_list.append(new_event)
        else:
            events_list.insert(index, new_event)

        return events_list

def save_data():
    global EVENTS, RESOURCES, NEXT_EVENT_ID

    data = {
        'events': EVENTS,
        'next_event_id': NEXT_EVENT_ID,
    }
    
    with open(FILEPATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, default=str)

def add_event(name, description, start, end, type, location, resources_ids, status=None):
    global NEXT_EVENT_ID
    from datetime import datetime
    #asegurar que start y end sean objetos datetime

    event = Event(
        start=start,
        end=end,
        name=name,
        type=type,
        location=location,
        status=status,
        resources=resources_ids,
        description=description
    )

    EVENTS[NEXT_EVENT_ID] = event.to_dict()
    NEXT_EVENT_ID += 1
    save_data()

    #agregar por aqui la llamada a la funcion que verficia si hay overlapping entre eventos, pero tambien tengo que 
    #que verificar si hay conflicto 

def list_events():
    return EVENTS.copy()

def get_event_by_id(event_id):
    for event in EVENT
def delete_event(event_id):



load_data()

print(list_events())