
def event_type_inclusion_restriction(type, resources):
    # pendiente definir bien los recursos y tipos de evento
    required_resources_by_event_type = {
        "Asedio a Castillo": ["Maquinaria de Asedio", "Arqueros", "Infantería Pesada"],
        "Batalla Naval": ["Almirante", "Armada"],
        "Batalla Campal": ["Infantería Pesada", "Caballería Pesada", "Arqueros"],
        "Torneo de Caballeros": ["Caballeros", "Ca"],
        "Emboscada": ["Infantería Ligera", "Caballería Ligera", "Arqueros"],
        "Misión de Espionaje": ["Maestro de Espías"]
    }

    needed_resources = required_resources_by_event_type[type]
    
    for required_resource in needed_resources:
        if required_resource not in resources:
            return False

    return True

def inclusion_restriction_between_resources(resources):
    inclusive_resources = {
        "Maquinaria de Asedio": "Ingeniero de Asedio",
        "Fuego Valyrio": "Piromante",
        "Caballero": "Espada",
        "Dragón": "Jinete de Sangre Valyria",
        "Vidriagón": "Tallador",
    }
    error = False
    if "Mercenario" in resources and "Oro" not in resources:
        error = True
    return error