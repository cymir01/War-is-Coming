import json
import os
import bisect
from datetime import datetime
from src.models.event import Event
from src.models.resource import Resource
from src.services.planner import validate_restrictions
from src.services.planner import resources_conflict_check
from data.default_data import default_data_function

#implementar try-except blocks en el comando add event
#implenmentar filtrado de eventos por atributo con funciones

FILEPATH = "src/services/war_planner.json"

EVENTS = [] #cambiar el codigo que gestiona events para que opere con lista y no dict
RESOURCES = {} #diccionario {id: Resource}
RESTRICTIONS = {}
NEXT_EVENT_ID = 1

def load_data():
    global EVENTS, RESOURCES, RESTRICTIONS, NEXT_EVENT_ID

    if not os.path.exists(FILEPATH): #revisar bien este bloque
        default_data = default_data_function() #corregir el idioma y el diseño de recursos
        resources_dict = default_data["resources"]
        RESOURCES = {int(id): Resource.create_robject_from_dict(r_data) for id, r_data in resources_dict.items()}
        RESTRICTIONS = default_data["restrictions"]
        EVENTS = []
        NEXT_EVENT_ID = default_data["next_event_id"]
        save_data()
        return
    
    try:
        with open(FILEPATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

            recursos_data = data.get('resources', {})
            RESOURCES = {int(resource_id): Resource.create_robject_from_dict(resource_data) for resource_id, resource_data in recursos_data.items()}

            RESTRICTIONS = data.get('restrictions', [])

            events_data = data.get('events', [])
            EVENTS = [Event.create_event_from_dict(event_data) for event_data in events_data]
            EVENTS.sort()  #usa __lt__ de la clase event

            NEXT_EVENT_ID = data.get('next_event_id', 1)

    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        #cargar datos por defecto en caso de error?

# def events_binary_cronological_sort(events_list, new_event):
#         if events_list == []:
#             return [new_event]
    
#         if new_event in events_list:
#             print("El evento ya existe")
#             return events_list
        
#         left = 0
#         right = len(events_list) - 1
#         index = len(events_list)

#         while left <= right:
#             midle = (left + right)//2
#             if new_event.get_start_date() < events_list[midle].get_start_date(): 
#                 index = midle
#                 right = midle - 1
#             else:
#                 left = midle + 1
    
#         if(index == len(events_list)):
#             events_list.append(new_event)
#         else:
#             events_list.insert(index, new_event)

#         return events_list

def save_data():
    #no necesito global aqui porque solo se leen las variables sin reasignar
    data = {
        "resources": {resource_id: resource.robject_to_dict() for resource_id, resource in RESOURCES.items()},
        "restrictions": RESTRICTIONS,
        'events': [event.event_to_dict() for event in EVENTS],
        'next_event_id': NEXT_EVENT_ID
    }
    with open(FILEPATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, default=str) #default=str para evitar fallo

def add_event(name, description, start, end, event_type, location, resources_ids, status="planned"):
    global NEXT_EVENT_ID

    for resource_id in resources_ids:
        if resource_id not in RESOURCES:
            raise ValueError(f"El recurso con id {resource_id} no existe")
    
    if isinstance(start, str):
        start = datetime.fromisoformat(start)

    if isinstance(end, str):
        end = datetime.fromisoformat(end)

    if end <= start:
        raise ValueError("La fecha final debe ser posterior a la inicial")

    new_event = Event(
        id=NEXT_EVENT_ID,
        name=name,
        description=description,
        start=start,
        end=end,
        event_type=event_type,
        location=location,
        status=status,
        resources_ids=resources_ids,
    )
    #pensar en como procesar la solicitud de un mismo recurso varias veces, valido o no?

    #en la funcion validate_restrictions en planner.py retorna mensajes de error para cada uno de los 3 casos
    #corregir este bloque condicional
    if not validate_restrictions(new_event, RESOURCES, RESTRICTIONS):
        raise ValueError("El evento incumple alguna restriccion de recursos o tipo de")
    
    if resources_conflict_check(new_event, EVENTS):
        raise ValueError("El evento pide recursos ya ocupados por otro evento programado")

    bisect.insort(EVENTS, new_event) #terminar de agregar __lt__ en Event
    NEXT_EVENT_ID += 1
    save_data()
    
def list_events():
    return EVENTS.copy()

def delete_event(event_id):
    """retorna True si se elimino el evento, False si no"""
    global EVENTS
    for index, event in enumerate(EVENTS):
        if event.id == event_id:
            del EVENTS[index] #INVESTIGAR SOBRE POP PARA USARLO SI ES MEJOR
            save_data()
            return True
        return False

def get_event_by_id(event_id):
    for event in EVENTS:
        if event.id == event_id:
            return event
    return None

def get_event_by_type():
    pass

def get_event_by_resource():
    pass

def get_events_in_range():
    pass

load_data()