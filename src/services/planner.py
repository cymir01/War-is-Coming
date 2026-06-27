from datetime import datetime, timedelta

#qgestionar en add_event() cuando el usuario pide un recurso (id) que no existe
#para que el usuario escoja los recursos tengo que listarlos con sus corresondientes id para que seleccione por id
DEFAULT_START_DATE = datetime(301, 1, 1, 0, 0)

def resources_conflict_check(new_event, existing_events):
    """funcion que devuelve False si no hay conflicto y True de haber"""
    for event in existing_events:
        if overlap(new_event, event):
            for resource_id in new_event.resources_ids:
                if resource_id in event.resources_ids:
                    return True
    return False

#UNIFICAR TODAS LAS FUNCIONES DE VALIDACION EN ESTA FUNCION
def validate_restrictions(new_event, resources, restrictions):
    """funcion que valida las restricciones de inclusion y exclusion entre recursos"""
    inclusion_restrictions = restrictions.get("resource_type_inclusion_restrictions", {})
    exclusion_restrictions = restrictions.get("rreesource_type_exclusion_restrictions", {})
    event_type_exclusion_restrictions = restrictions.get("event_type_exclusion_restrictions", {})
    event_type_inclusion_restrictions = restrictions.get("event_type_inclusion_restrictions", {})
    houses_exclusion_restrictions = restrictions.get("house_exclusion_restrictions", {})
    character_exclusion_restrictions = restrictions.get("character_exclusion_restrictions", {})

#terminar los strings de error. Ademas puedo referir los recursos especificos con problemas
    exc_rest_bool, exclusive_resource = validate_event_type_exclusion_restriction(new_event, exclusion_restrictions)
    inc_rest_bool, required_resource = validate_event_type_inclusion_restriction(new_event, inclusion_restrictions)
    et_inc_rest_bool, needed_resource = validate_event_type_inclusion_restriction(new_event, event_type_inclusion_restrictions)
    et_exc_rest_bool, forbbiden_resource = validate_event_type_exclusion_restriction(new_event, event_type_exclusion_restrictions)
    houses_exc_bool, exclusive_house = validate_houses_exclusion_restrictions(new_event, resources, houses_exclusion_restrictions)

    
    return True, ''

def validate_resource_type_inclusion_restrictions(new_event, resource_type_inclusion_restrictions):
    """devuelve True si se cumplen las restricciones de inclusion y False si no"""
    new_event_resources_ids = set(new_event.resources_ids)
    
    for resource, required_resources in resource_type_inclusion_restrictions.items():
        resource = int(resource)
        if resource in new_event_resources_ids:
            for required_id in required_resources:
                required_id = int(required_id)
                if required_id not in new_event_resources_ids:
                    return False, f"error! el recurso {resource} requiere el recurso {required_id}"
    return True, ""

def validate_resource_type_exclusion_restrictions(new_event, resource_type_exclusion_restrictions):
    """True si no se viola ninguna restriccion, False en caso contrario"""
    new_event_resources_ids = set(new_event.resources_ids)
    for resource, exclusive_resources in resource_type_exclusion_restrictions.items():
        resource = int(resource)
        if resource in new_event_resources_ids:
            for exclusive_resource in exclusive_resources:
                exclusive_resource = int(exclusive_resource)
                if exclusive_resource in new_event_resources_ids:
                    return False, f"error: el evento incluye recursos excluyentes: {resource} y {exclusive_resource}"
    return True, ''

#la funcion debe usar el atributo tipo de los recursos
def validate_event_type_inclusion_restriction(new_event, resources, event_type_inclusion_restrictions):
    event_type = new_event.even_type
    resources_ids_new_event = set(new_event.resources_ids)
    resources_type_new_event = set()

    for resource_id in resources_ids_new_event:
        if resource_id in resources:
            resource_type = resources[resource_id].resource_type
            if resource_type:
                resources_type_new_event.add(resource_type)
        
    if event_type in event_type_inclusion_restrictions:
        required_resources_type = event_type_inclusion_restrictions[event_type]
        for required_r_type in required_resources_type:
            if required_r_type not in resources_ids_new_event:
                return False, f"Error: el evento tipo {event_type} requiere el tipo de recurso {required_r_type}"
    return True, ""

#idem
def validate_event_type_exclusion_restriction(new_event, event_type_exclusion_restrictions):
    event_type = new_event.event_type
    resources_ids_new_event = set(new_event.resources_ids)

    if event_type in event_type_exclusion_restrictions:
        forbbiden_resources = event_type_exclusion_restrictions[event_type]
        for forbbiden_resource in forbbiden_resources:
            forbbiden_resource = int(forbbiden_resource)
            if forbbiden_resource in resources_ids_new_event:
                return False, f"Error: el evento tipo {event_type} no puede usar el recurso {forbbiden_resource}"
    return True, ''

def validate_houses_exclusion_restrictions(new_event, resources, houses_exclusion_restrictions):
    houses_new_event = set()
    for resource_id in new_event.resources_ids:
        if resource_id in resources:
            house = resources[resource_id].house
            if house:
                houses_new_event.add(house)
    for house in houses_new_event:
        if house in houses_exclusion_restrictions:
            enemy_houses = houses_exclusion_restrictions[house]
            for enemy_house in enemy_houses:
                if enemy_house in houses_new_event:
                    return False, f"error: la casa {house} no puede aliarse con la casa {enemy_house}"
    return True, ""

# Debes implementar una función inteligente que, dado un evento y los recursos que necesita, sea capaz de analizar el calendario y 
# sugerir el próximo intervalo de tiempo disponible donde se pueda realizar sin conflictos ni violaciones de restricciones.
def get_event_start(event):
    return event.start

#en esta funcion tengo que validar las restricciones llamando a validate_restrictions 
# y ademas chequear conflicto de recrusos llamando a conflict_resoruces_check
# la validacion del hueco estaria separada de la busqueda del hueco
def is_slot_valid(start_time, end_time, resources_ids, sorted_events):
    for event in sorted_events:
        if max(start_time, event.start) < min(end_time, event.end):
            for resource_id in resources_ids:
                if resource_id in event.resources_ids:
                    return False
    return True

#usar la fecha de inicio que pide el usuario, no now() porque el calendario que debe usar el programa es ficticio
def find_next_available_time_slot(resource_ids, duration_hours, start_from, max_days=30, existing_events=None, event_type=None, step_minutes=5):
    if existing_events is None:
        existing_events = []
    if start_from is None:
        start_from = DEFAULT_START_DATE

    sorted_events = sorted(existing_events, key=get_event_start)

    end_limit = start_from + timedelta(days=max_days)
    current_time = start_from

    for event in sorted_events:
        if event.end <= current_time:
            continue
    
    if event.start > current_time:
        gap_hours = (event.start - current_time).total_seconds() / 3600.0
        if gap_hours >= duration_hours:
            candidate_end = current_time + timedelta(hours=duration_hours)
            if candidate_end <= event.start:
                if is_slot_valid(current_time, candidate_end, resource_ids, sorted_events):
                    return current_time, candidate_end
    
    for rid in resource_ids:
        if rid in event.resources_ids:
            current_time = max(current_time, event.end)
            break
    if (end_limit - current_time).total_seconds() / 3600.0 >= duration_hours:
        candidate_end = current_time + timedelta(hours=duration_hours)
        if candidate_end <= end_limit:
            if is_slot_valid(current_time, candidate_end, resource_ids, sorted_events):
                return current_time, candidate_end

    return None

def overlap(event1, event2):
    '''
    esta funcion devuelve True si se solapan los eventos y False en caso contrario
    '''
    return max(event1.start, event2.start) < min(event1.end, event2.end)