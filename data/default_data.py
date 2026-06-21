def default_data_function():
    default_data = {
        "resources": {
        "1": { "id": 1, "name": "Infantería pesada Lannister", "house": "Lannister" },
        "2": { "id": 2, "name": "Caballería Lannister", "house": "Lannister" },
        "3": { "id": 3, "name": "Maquinaria asedio Lannister", "house": "Lannister" },
        "4": { "id": 4, "name": "Infantería pesada Stark", "house": "Stark" },
        "5": { "id": 5, "name": "Caballería Stark", "house": "Stark" },
        "6": { "id": 6, "name": "Arqueros Lannister", "house": "Lannister" },
        "7": { "id": 7, "name": "Arqueros Stark", "house": "Stark" },
        "8": { "id": 8, "name": "Maestro de Guerra Lannister", "house": "Lannister" },
        "9": { "id": 9, "name": "Eddard Stark", "house": "Stark" },
        "10": { "id": 10, "name": "Fuego Valyrio", "house": "Targaryen" },
        "11": { "id": 11, "name": "Piromante", "house": "Targaryen" },
        "12": { "id": 12, "name": "Espada de Acero Valyrio", "house": "Targaryen" }
        },

        "enemy_houses": {
            "Lannister": ["Martell", "Stark", "Targaryen", "Tully"],
            "Stark": ["Lannister", "Bolton", "Greyjoy"],
            "Targaryen": ["Baratheon", "Lannister"],
            "Baratheon": ["Targaryen"],
            "Tully": ["Lannister", "Frey"],
            "Martell": ["Lannister"],
            "Greyjoy": ["Stark"],
            "Bolton": ["Stark"],
            "Frey": ["Stark", "Tully"]
        },

        "restrictions": {
            "inclusion_restrictions": {
                "3": ["1"],              #Maquinaria asedio requiere infantería pesada
                "10": ["11"],            #Fuego Valyrio requiere Piromante
                "8": ["1", "3"]          #Maestre de Guerra requiere infantería y maquinaria
            },
            "exclusion_restrictions": {
                "1": ["4"],              #Infantería Lannister no con Infantería Stark
                "2": ["5"],              #Caballería Lannister no con Caballería Stark
                "3": ["5"],              #Maquinaria Lannister no con Caballería Stark
                "10": ["3"]              #Fuego Valyrio no con Maquinaria (seguridad)
            },
            "inclusion_por_tipo_evento": {
                "Asedio": ["3"],         #evento "Asedio" DEBE incluir maquinaria
                "Batalla Naval": ["10"], #evento "Batalla Naval" DEBE incluir Fuego Valyrio
                "Asalto": ["1", "2"],    #evento "Asalto" DEBE incluir infantería y caballería
                "Defensa": ["1", "6"]    #evento "Defensa" DEBE incluir infantería y arqueros
            },
            "exclusion_por_tipo_evento": {
                "Emboscada": ["3"],      #evento "Emboscada" NO puede usar maquinaria
                "Batalla Naval": ["2", "5"],  #Batalla Naval NO puede usar caballería
                "Asedio": ["2", "5"],    #Asedio NO puede usar caballería
                "Defensa": ["2"]         #Defensa NO puede usar caballería
            }
        },

        "events": [],
        "next_event_id": 1
    }
    return default_data
