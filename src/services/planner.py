from datetime import datetime
from datetime import datetime, timedelta
from models.event import Event

def resources_conflict_check(new_event, existing_events):
    """funcion que devuelve False si no hay conflicto y True de haber"""
    for event in existing_events:
        if overlap(new_event, event):
            for resource_id in new_event.resources_ids:
                if resource_id in event.resources_ids:
                    return True
    return False


def validate_restrictions(new_event, resources, restrictions):
    """funcion que valida las restricciones de inclusion y exclusion entre recursos"""
    inclusion_restrictions = restrictions.get("inclusion_restrictions", {})
    exclusion_restrictions = restrictions.get("exclusion_restrictions", {})
    event_type_exclusion_restrictions = restrictions.get("event_type_exclusion_restrictions", {})
    event_type_inclusion_restrictions = restrictions.get("event_type_inclusion_restrictions", {})
    houses_exclusion_restrictions = restrictions.get("houses_exclusion_restrictions", {})

    if not validate_exclusion_restrictions_between_resources(new_event, exclusion_restrictions):
        return False
    if not validate_inclusion_restrictions_between_resources(new_event, inclusion_restrictions):
        return False
    if not validate_event_type_exclusion_restriction(new_event, event_type_exclusion_restrictions):
        return False
    if not validate_event_type_inclusion_restriction(new_event, event_type_inclusion_restrictions):
        return False
    if not validate_houses_exclusion_restrictions(new_event, resources, houses_exclusion_restrictions):
        return False
    
    return True

def validate_inclusion_restrictions_between_resources(new_event, inclusion_restrictions):
    """devuelve True si se cumplen las restricciones de inclusion y False si no"""
    new_event_resources_ids = set(new_event.resources_ids)
    for resource, required_resources in inclusion_restrictions.items():
        resource = int(resource)
        if resource in new_event_resources_ids:
            for required_id in required_resources:
                required_id = int(required_id)
                if required_id not in new_event_resources_ids:
                    return False
    return True

def validate_exclusion_restrictions_between_resources(new_event, exclusion_restrictions):
    """True si no se viola ninguna restriccion, False en caso contrario"""
    new_event_resources_ids = set(new_event.resources_ids)
    for resource, exclusive_resources in exclusion_restrictions.items():
        resource = int(resource)
        if resource in new_event_resources_ids:
            for exclusive_resource in exclusive_resources:
                exclusive_resource = int(exclusive_resource)
                if exclusive_resource in new_event_resources_ids:
                    return False
    return True

def validate_event_type_inclusion_restriction(new_event, event_type_inclusion_restrictions):
    event_type = new_event.even_type
    resources_ids_new_event = set(new_event.resources_ids)

    if event_type in event_type_inclusion_restrictions:
        required_resources = event_type_inclusion_restrictions[event_type]
        for required_resource in required_resources:
            required_resource = int(required_resource)
            if required_resource not in resources_ids_new_event:
                return False
    return True


def validate_event_type_exclusion_restriction(new_event, event_type_exclusion_restrictions):
    event_type = new_event.event_type
    resources_ids_new_event = set(new_event.resources_ids)

    if event_type in event_type_exclusion_restrictions:
        forbbiden_resources = event_type_exclusion_restrictions[event_type]
        for forbbiden_resource in forbbiden_resources:
            forbbiden_resource = int(forbbiden_resource)
            if forbbiden_resource in resources_ids_new_event:
                return False
    return True

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
                    return False
    return True


# Debes implementar una función inteligente que, dado un evento y los recursos que necesita, sea capaz de analizar el calendario y 
# sugerir el próximo intervalo de tiempo disponible donde se pueda realizar sin conflictos ni violaciones de restricciones.
def find_next_available_time_slot(resource_ids, duration_hours, start_from=None, max_days=30):
    pass

def overlap(event1, event2):
    '''
    esta funcion devuelve True si se solapan los eventos y False en caso contrario
    '''
    return max(event1.start, event2.start) < min(event1.end, event2.end)