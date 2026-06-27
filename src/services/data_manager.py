import json
import os
import bisect
from datetime import datetime
from src.models.event import Event
from src.models.resource import Resource
from src.services.planner import validate_restrictions
from src.services.planner import resources_conflict_check

#implementar try-except blocks en el comando add event
#implenmentar filtrado de eventos por atributo con funciones

FILEPATH = "data/war_planner.json"
DEFAULT_DATA = "data/default_data.json"

EVENTS = [] #cambiar el codigo que gestiona events para que opere con lista y no dict
RESOURCES = {}
RESTRICTIONS = {}
NEXT_EVENT_ID = 1

def load_data():
    global EVENTS, RESOURCES, RESTRICTIONS, NEXT_EVENT_ID
#ARREGLAR
    if not os.path.exists(FILEPATH): #revisar bien este bloque
        try:
            with open(DEFAULT_DATA, 'r', encoding='utf-8') as f:
                default_data = json.load(f)
        except FileNotFoundError:
            print("No se encontró default_data.json. Usando datos vacíos...")
            default_data = {"resources": {}, "restrictions": {}, "events": [], "next_event_id": 1}
        resources_dict = default_data.get("resources", {})
        RESOURCES = {int(id): Resource.create_robject_from_dict(r_data) for id, r_data in resources_dict.items()}
        RESTRICTIONS = default_data.get("restrictions", {})
        EVENTS = []
        NEXT_EVENT_ID = default_data.get("next_event_id", 1)
        save_data()
        return
    
    try:
        with open(FILEPATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            recursos_data = data.get('resources', {})
            RESOURCES = {int(resource_id): Resource.create_robject_from_dict(resource_data) for resource_id, resource_data in recursos_data.items()}
            RESTRICTIONS = data.get('restrictions', {})
            events_data = data.get('events', [])
            EVENTS = [Event.create_event_from_dict(event_data) for event_data in events_data]
            EVENTS.sort()  #ordena cronológicamente usando __lt__ de Event
            NEXT_EVENT_ID = data.get('next_event_id', 1)
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        load_default_data()
        return
        #cargar datos por defecto en caso de error

def load_default_data():
    global EVENTS, RESOURCES, RESTRICTIONS, NEXT_EVENT_ID
    try:
        with open(DEFAULT_DATA, 'r', encoding='utf-8') as f:
            default_data = json.load(f)
        resources_dict = default_data.get("resources", {})
        RESOURCES = {int(id): Resource.create_robject_from_dict(r_data) for id, r_data in resources_dict.items()}
        RESTRICTIONS = default_data.get("restrictions", {})
        EVENTS = []
        NEXT_EVENT_ID = default_data.get("next_event_id", 1)
        save_data()
    except Exception as e:
        print(f"Error al cargar datos por defecto: {e}")
        RESOURCES = {}
        RESTRICTIONS = {}
        EVENTS = []
        NEXT_EVENT_ID = 1

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

#VERIFICAR QUE SE COMUNIQUE BIEN CON EL COMANDO ADD_EVENT
def add_event(name, description, start, end, event_type, location, resources_ids, status="planned"):
    global NEXT_EVENT_ID

    for resource_id in resources_ids:
        if resource_id not in RESOURCES:
            raise ValueError(f"El recurso con id {resource_id} no existe")
    
    #elimina duplicados de la lista de recuross
    resources_ids = list(set(resources_ids))

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
    
    bool_restrictions, mesage = validate_restrictions(new_event, RESOURCES, RESTRICTIONS)
    if not bool_restrictions:
        return False, mesage
    
    #ESPECIFICAR EL RECURSO OCUPADO
    if resources_conflict_check(new_event, EVENTS):
        return False, "Conflicto de recursos: algún recurso ya está ocupado en ese horario"

    bisect.insort(EVENTS, new_event) #usa internamente el metodo __lt__ de la clase Event
    NEXT_EVENT_ID += 1
    save_data()
    return True, new_event.id
    
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

#>>>>>>>FUNCIONES AUXILIARES POTENCIALMENTE UTILES>>>>>>
def get_event_by_id(event_id):
    for event in EVENTS:
        if event.id == event_id:
            return event
    return None

def get_event_by_type(event_type):
    """filtra eventos por tipo"""
    return [event for event in EVENTS if event.event_type == event_type]

def get_event_by_resource(resource_id):
    """filtra eventos que usan cierto recurso específico"""
    return [event for event in EVENTS if resource_id in event.resources_ids]

#puedo usarla para:
#OPTIMIZAR LA BUSQUEDA DE HUECOS
#nuevos comandos como 'events of the week ', etc
#geenerar reportes y estadisiticas
#verificar disponibilidad de un recurso en un rango dado
#ver que eventos hay en un periodo especifico
#etc
def get_events_in_range(start, end):
    """devuelve eventos que solapan el rango [start, end]"""
    return [event for event in EVENTS if max(event.start, start) < min(event.end, end)]
#>>>>>>>>>>>>>>>>>

load_data()