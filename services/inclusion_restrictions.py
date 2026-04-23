
def event_type_inclusion_restriction(event_type, dict_resources):
    # pendiente definir bien los recursos y tipos de evento
    required_resources_by_event_type = {
        "Asedio a Castillo": ["Maquinaria de Asedio", "Arqueros", "Infantería Pesada"],
        "Batalla Naval": ["Almirante", "Armada"],
        "Batalla Campal": ["Infantería Pesada", "Caballería Pesada", "Arqueros"],
        "Emboscada": ["Infantería Ligera", "Caballería Ligera", "Arqueros"],
        "Misión de Espionaje": ["Maestro de espías"],
        "Misión diplomática": ["Embajador"]
    }

    needed_resources = required_resources_by_event_type[event_type]
    
    for needed_resource in needed_resources:
        if needed_resource not in dict_resources:
            return False

    return True

def inclusion_restriction_between_resources(resources):
    inclusive_resources = {
        "Maquinaria de Asedio": ["Hijo del Lecho de Pulgas"],
        "Fuego Valyrio": ["Piromante"],
        "Dragón": ["Jinete de sangre valyria"],
        "Espada de acero valyrio": ["Caballero de linaje noble"],
        "Dothraki": ["Arakh", "Caballo"],
        "Mercenarios": ["Oro"]
    }

# inclusion_restriction_between_resources(["4"])
print(event_type_inclusion_restriction("Asedio a Castillo"))