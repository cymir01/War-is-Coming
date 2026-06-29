from datetime import datetime, timedelta
from src.models.event import Event
DEFAULT_START_DATE = datetime(301, 1, 1, 0, 0)

def resources_conflict_check(new_event, existing_events):
    """funcion que devuelve False si no hay conflicto y True de haber"""
    for event in existing_events:
        if overlap(new_event, event):
            for resource_id in new_event.resources_ids:
                if resource_id in event.resources_ids:
                    return True, f"El recurso {resource_id} ya está ocupado por otro evento en el intervalo solicitado"
    return False, ''

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
                    return False, f"Error: el recurso tipo '{required_type}' requiere el recurso tipo '{req_type}'"
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


def find_next_available_time_slot(resources_ids, duration_hours, start_from=None, max_days=30, existing_events=None, resources=None, restrictions=None, event_type=None):
    if existing_events is None:
        existing_events = []
    if start_from is None:
        start_from = DEFAULT_START_DATE

    if not resources_ids:
        return None, None
        
    resources_ids = list(set(resources_ids))

    if event_type is None and restrictions:
        event_type = "Batalla campal"
    
    sorted_events = sorted(existing_events, key=lambda e: e.start)
    
    end_limit = start_from + timedelta(days=max_days)
    
    current_time = start_from
    
    def check_resource_conflict(start_time, end_time, resources_ids, events):
        for event in events:
            if max(start_time, event.start) < min(end_time, event.end):
                for resource_id in resources_ids:
                    if resource_id in event.resources_ids:
                        return False
        return True
    
    def check_restrictions(start_time, end_time, resources_ids, event_type, resources, restrictions):
        if resources is None or restrictions is None:
            return True
        
        temp_event = Event(
            id=-1,
            name="temp",
            start=start_time,
            end=end_time,
            event_type=event_type,
            resources_ids=resources_ids
        )
        
        valid, _ = validate_restrictions(temp_event, resources, restrictions)
        return valid
    
    def is_valid_slot(start_time, end_time, resources_ids, events, resources, restrictions, event_type):
        if not check_resource_conflict(start_time, end_time, resources_ids, events):
            return False
        
        if not check_restrictions(start_time, end_time, resources_ids, event_type, resources, restrictions):
            return False
        
        return True
    
    if not sorted_events:
        temp_time = start_from
        while temp_time < end_limit:
            candidate_end = temp_time + timedelta(hours=duration_hours)
        
            if candidate_end > end_limit:
                break
        
            if is_valid_slot(temp_time, candidate_end, resources_ids, sorted_events, resources, restrictions, event_type):
                return temp_time, candidate_end
            temp_time += timedelta(hours=1)

        return None, None
    
    for event in sorted_events:
        if event.end <= current_time:
            continue
        
        if event.start > current_time:
            gap_duration = (event.start - current_time).total_seconds() / 3600.0
            
            if gap_duration >= duration_hours:
                temp_time = current_time

                while temp_time + timedelta(hours=duration_hours) <= event.start:
                    candidate_end = temp_time + timedelta(hours=duration_hours)
                    if is_valid_slot(temp_time, candidate_end, resources_ids, sorted_events, resources, restrictions, event_type):
                        return temp_time, candidate_end
                    temp_time += timedelta(hours=1)
        
        uses_resources = any(res_id in event.resources_ids for res_id in resources_ids)
        if uses_resources:
            current_time = max(current_time, event.end)
        else:
            if event.end > current_time:
                current_time = max(current_time, event.end)

    remaining_hours = (end_limit - current_time).total_seconds() / 3600.0
    
    if remaining_hours >= duration_hours:
        temp_time = current_time
        while temp_time + timedelta(hours=duration_hours) <= end_limit:
            candidate_end = temp_time + timedelta(hours=duration_hours)

            if is_valid_slot(temp_time, candidate_end, resources_ids, sorted_events, resources, restrictions, event_type):
                return temp_time, candidate_end
            
            temp_time += timedelta(hours=1)

    return None, None

def overlap(event1, event2):
    '''
    esta funcion devuelve True si se solapan los eventos y False en caso contrario
    '''
    return max(event1.start, event2.start) < min(event1.end, event2.end)