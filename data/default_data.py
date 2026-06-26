def default_data_function():
    default_data = def default_data_function():
    return {
        "resources": {
            "1": {"id": 1, "name": "Infantería pesada Lannister", "type": "Infantería pesada", "house": "Lannister"},
            "2": {"id": 2, "name": "Caballería pesada Lannister", "type": "Caballería pesada", "house": "Lannister"},
            "3": {"id": 3, "name": "Maquinaria de asedio Lannister", "type": "Maquinaria de asedio", "house": "Lannister"},
            "4": {"id": 4, "name": "Infantería pesada Stark", "type": "Infantería pesada", "house": "Stark"},
            "5": {"id": 5, "name": "Caballería pesada Stark", "type": "Caballería pesada", "house": "Stark"},
            "6": {"id": 6, "name": "Arqueros Lannister", "type": "Arqueros", "house": "Lannister"},
            "7": {"id": 7, "name": "Arqueros Stark", "type": "Arqueros", "house": "Stark"},
            "8": {"id": 8, "name": "Maestro de Guerra Lannister", "type": "Maestro de guerra", "house": "Lannister"},
            "9": {"id": 9, "name": "Eddard Stark", "type": "Personaje", "house": "Stark"},
            "10": {"id": 10, "name": "Fuego Valyrio", "type": "Fuego Valyrio", "house": "Targaryen"},
            "11": {"id": 11, "name": "Piromante", "type": "Piromante", "house": "Targaryen"},
            "12": {"id": 12, "name": "Espada de Acero Valyrio", "type": "Espada de acero valyrio", "house": "Targaryen"},
            "13": {"id": 13, "name": "Mercenarios", "type": "Mercenarios", "house": None},
            "14": {"id": 14, "name": "Oro", "type": "Oro", "house": None},
            "15": {"id": 15, "name": "Dragón", "type": "Dragón", "house": None},
            "16": {"id": 16, "name": "Ingeniero de asedio Lannister", "type": "Ingeniero de asedio", "house": "Lannister"},
            "17": {"id": 17, "name": "Ingeniero de asedio Stark", "type": "Ingeniero de asedio", "house": "Stark"},
            "18": {"id": 18, "name": "Almirante Lannister", "type": "Almirante", "house": "Lannister"},
            "19": {"id": 19, "name": "Almirante Stark", "type": "Almirante", "house": "Stark"},
            "20": {"id": 20, "name": "Caballero Lannister", "type": "Caballero", "house": "Lannister"},
            "21": {"id": 21, "name": "Caballero Stark", "type": "Caballero", "house": "Stark"}
        },
        "restrictions": {
            "type_inclusion_restrictions": {
                "Maquinaria de asedio": ["Ingeniero de asedio"],
                "Fuego Valyrio": ["Piromante"],
                "Maestro de guerra": ["Infantería pesada", "Maquinaria de asedio"]
            },
            "type_exclusion_restrictions": {
                "Caballería pesada": ["Maquinaria de asedio"]
            },
            "house_exclusion_restrictions": {
                "Lannister": ["Stark", "Targaryen", "Tully", "Martell"],
                "Stark": ["Lannister", "Bolton", "Greyjoy"],
                "Targaryen": ["Baratheon", "Lannister"],
                "Baratheon": ["Targaryen"],
                "Tully": ["Lannister", "Frey"],
                "Martell": ["Lannister"],
                "Greyjoy": ["Stark"],
                "Bolton": ["Stark"],
                "Frey": ["Stark", "Tully"]
            },
            "event_type_inclusion_restrictions": {
                "Asedio": ["Maquinaria de asedio"],
                "Batalla Naval": ["Fuego Valyrio"],
                "Asalto": ["Infantería pesada", "Caballería pesada"],
                "Defensa": ["Infantería pesada", "Arqueros"]
            },
            "event_type_exclusion_restrictions": {
                "Emboscada": ["Maquinaria de asedio"],
                "Batalla Naval": ["Caballería pesada"],
                "Asedio": ["Caballería pesada"],
                "Defensa": ["Caballería pesada"]
            }
        },
        "events": [],
        "next_event_id": 1
    }
    return default_data
