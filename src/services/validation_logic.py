from datetime import datetime

def validate_date_input(year, month, day, hours, minutes):
    try:
        date = datetime(year, month, day, hours, minutes)
        return True, "", date

    except ValueError as e:
        return False, f"[red]Error de fecha: {str(e)}. Intente de nuevo[/red]", None

    
def exclusion_restriction_houses(houses):
    enemy_houses_lists = {"Lannister": ["Martell", "Stark", "Targaryen", "Tully"],
                    "Stark": ["Lannister", "Bolton", "Greyjoy"],
                    "Targaryen": ["Baratheon", "Lannister"],
                    "Baratheon": ["Targaryen"],
                    "Tully": ["Lannister", "Frey"],
                    "Martell": ["Lannister"],
                    "Greyjoy": ["Stark"],
                    "Bolton": ["Stark"],
                    "Frey": ["Stark", "Tully"]}
    
    # for house in houses:
    #     enemy_houses = enemy_houses_lists[house]
    #     for enemy_houses in en
        
exclusion_restriction_houses(["Lannister"])

def exclusion_restriction_special_resources(resources):
    # pensar en exclusiones entre recursos especiales. Quiza cierto recurso especifico que aparece en la serie no
    # no puede combinarse con otra cosa especifica que aparece en la serie. En el programa aparecerian como recursos especiales
    pass

def event_type_exclusion_restriction():
    # emobscada excluyente de maquinaria de asedio, etc
    pass


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

def event_type_inclusion_restriction():
    pass
# inclusion_restriction_between_resources(["4"])
print(event_type_inclusion_restriction("Asedio a Castillo"))