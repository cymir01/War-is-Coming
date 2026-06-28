from datetime import datetime, timedelta
DEFAULT_START_DATE = datetime(301, 1, 1, 0, 0)
#qgestionar en add_event() cuando el usuario pide un recurso (id) que no existe (lanza error)

def resources_conflict_check(new_event, existing_events):
    """funcion que devuelve False si no hay conflicto y True de haber"""
    for event in existing_events:
        if overlap(new_event, event):
            for resource_id in new_event.resources_ids:
                if resource_id in event.resources_ids:
                    return True
    return False

def validate_restrictions(new_event, resources, restrictions):
    """funcion que valida todas las restricciones (por tipo de recurso, tipo de eventp y casas)"""
    resource_type_inclusion_restrictions = restrictions.get("resource_type_inclusion_restrictions", {})
    resource_type_exclusion_restrictions = restrictions.get("resource_type_exclusion_restrictions", {})
    event_type_exclusion_restrictions = restrictions.get("event_type_exclusion_restrictions", {})
    event_type_inclusion_restrictions = restrictions.get("event_type_inclusion_restrictions", {})
    houses_exclusion_restrictions = restrictions.get("house_exclusion_restrictions", {})

    valid, mesage = validate_resource_type_inclusion_restrictions(new_event, resources, resource_type_inclusion_restrictions)
    if not valid:
        return False, mesage

    valid, mesage = validate_resource_type_exclusion_restrictions(new_event, resources, resource_type_exclusion_restrictions)
    if not valid:
        return False, mesage

    valid, mesage = validate_event_type_inclusion_restriction(new_event, resources, event_type_inclusion_restrictions)
    if not valid:
        return False, mesage

    valid, mesage = validate_event_type_exclusion_restriction(new_event, resources, event_type_exclusion_restrictions)
    if not valid:
        return False, mesage

    valid, mesage = validate_houses_exclusion_restrictions(new_event, resources, houses_exclusion_restrictions)
    if not valid:
        return False, mesage
    
    return True, ''

def validate_resource_type_inclusion_restrictions(new_event, resources, resource_type_inclusion_restrictions):
    """devuelve True si se cumplen las restricciones de inclusion y False si no"""
    resource_types = set()
    for rid in new_event.resources_ids:
        if rid in resources:
            r_type = resources[rid].resource_type
            if r_type:
                resource_types.add(r_type)

    for required_type, required_with in resource_type_inclusion_restrictions.items():
        if required_type in resource_types:
            for req_type in required_with:
                if req_type not in resource_types:
                    return False, f"Error: el recurso tipo '{required_type}' requiere el tipo '{req_type}'"
    return True, ""

def validate_resource_type_exclusion_restrictions(new_event, resources, resource_type_exclusion_restrictions):
    """True si no se viola ninguna restriccion, False en caso contrario"""
    resource_types = set()
    for rid in new_event.resources_ids:
        if rid in resources:
            r_type = resources[rid].resource_type
            if r_type:
                resource_types.add(r_type)
    
    for type_a, excluded_types in resource_type_exclusion_restrictions.items():
        if type_a in resource_types:
            for type_b in excluded_types:
                if type_b in resource_types:
                    return False, f"Error: los tipos '{type_a}' y '{type_b}' son excluyentes"
    return True, ''

#DA PROBLEMAS
def validate_event_type_inclusion_restriction(new_event, resources, event_type_inclusion_restrictions):
    event_type = new_event.event_type
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
            if required_r_type not in resources_type_new_event:
                return False, f"Error: el evento tipo {event_type} requiere el tipo de recurso {required_r_type}"
    return True, ""


def validate_event_type_exclusion_restriction(new_event, resources, event_type_exclusion_restrictions):
    event_type = new_event.event_type
    resources_ids_new_event = set(new_event.resources_ids)
    resources_type_new_event = set()

    for rid in resources_ids_new_event:
        if rid in resources:
            r_type = resources[rid].resource_type
            if r_type:
                resources_type_new_event.add(r_type)

    if event_type in event_type_exclusion_restrictions:
        forbidden_types = event_type_exclusion_restrictions[event_type]
        for forbidden_type in forbidden_types:
            if forbidden_type in resources_type_new_event:
                return False, f"Error: el evento tipo '{event_type}' no puede usar el tipo de recurso '{forbidden_type}'"
    return True, ''

def validate_houses_exclusion_restrictions(new_event, resources, houses_exclusion_restrictions):
    houses_new_event = set()
    new_event_resources_ids = set(new_event.resources_ids)

    for resource_id in new_event_resources_ids:
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

def get_event_start(event):
    return event.start

def is_slot_valid(start_time, end_time, resources_ids, sorted_events):
    """comprueba que ningún recurso esté ocupado en el intervalo"""
    for event in sorted_events:
        if max(start_time, event.start) < min(end_time, event.end):
            for resource_id in resources_ids:
                if resource_id in event.resources_ids:
                    return False
    return True

def find_next_available_time_slot(resource_ids, duration_hours, start_from, max_days=30, existing_events=None, resources=None, restrictions=None, event_type=None):
    if existing_events is None:
        existing_events = []
    if start_from is None:
        start_from = DEFAULT_START_DATE

    sorted_events = sorted(existing_events, key=get_event_start)
    end_limit = start_from + timedelta(days=max_days)
    current_time = start_from

    #si el evento ya termino lo saltamos
    for event in sorted_events:
        if event.end <= current_time:
            continue
    
    #si hay un hueco entre current_time y event.start
    if event.start > current_time:
        gap_hours = (event.start - current_time).total_seconds() / 3600.0
        if gap_hours >= duration_hours:
            candidate_end = current_time + timedelta(hours=duration_hours)
            if candidate_end <= event.start:
                if is_slot_valid(current_time, candidate_end, resource_ids, sorted_events):
                    if resources is not None and restrictions is not None and event_type is not None:
                        from src.models.event import Event
                        temporal_event = Event(
                            id=-1,
                            name="temp",
                            start=current_time,
                            end=candidate_end,
                            event_type=event_type,
                            resources_ids=resource_ids
                        )
                        valid, mesage = validate_restrictions(temporal_event, resources, restrictions)
                        if not valid:
                            pass #seguimos buscando si no cumple...
                        else:
                            return current_time, candidate_end
                    else:
                        return current_time, candidate_end
                    
        for rid in resource_ids:
            if rid in event.resources_ids:
                current_time = max(current_time, event.end)
                break

    if (end_limit - current_time).total_seconds() / 3600.0 >= duration_hours:
        candidate_end = current_time + timedelta(hours=duration_hours)
        if candidate_end <= end_limit:
            if is_slot_valid(current_time, candidate_end, resource_ids, sorted_events):
                if resources is not None and restrictions is not None and event_type is not None:
                    from src.models.event import Event
                    temporal_event = Event(
                        id=-1,
                        name="temp",
                        start=current_time,
                        end=candidate_end,
                        event_type=event_type,
                        resources_ids=resource_ids
                    )
                    valid, mesage = validate_restrictions(temporal_event, resources, restrictions)
                    if valid:
                        return current_time, candidate_end
                else:
                    return current_time, candidate_end
    return None, None

def overlap(event1, event2):
    '''
    esta funcion devuelve True si se solapan los eventos y False en caso contrario
    '''
    return max(event1.start, event2.start) < min(event1.end, event2.end)