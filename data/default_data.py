def default_data_function():
    default_data = {
        "recursos": {
        "1": { "id": 1, "nombre": "Infantería pesada Lannister", "casa": "Lannister" },
        "2": { "id": 2, "nombre": "Caballería Lannister", "casa": "Lannister" },
        "3": { "id": 3, "nombre": "Maquinaria asedio Lannister", "casa": "Lannister" },
        "4": { "id": 4, "nombre": "Infantería pesada Stark", "casa": "Stark" },
        "5": { "id": 5, "nombre": "Caballería Stark", "casa": "Stark" },
        "6": { "id": 6, "nombre": "Arqueros Lannister", "casa": "Lannister" },
        "7": { "id": 7, "nombre": "Arqueros Stark", "casa": "Stark" },
        "8": { "id": 8, "nombre": "Maestro de Guerra Lannister", "casa": "Lannister" },
        "9": { "id": 9, "nombre": "Eddard Stark", "casa": "Stark" },
        "10": { "id": 10, "nombre": "Fuego Valyrio", "casa": "Targaryen" },
        "11": { "id": 11, "nombre": "Piromante", "casa": "Targaryen" },
        "12": { "id": 12, "nombre": "Espada de Acero Valyrio", "casa": "Targaryen" }
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

        "restricciones": {
            "inclusion_entre_recursos": {
                "3": ["1"],              #Maquinaria asedio requiere infantería pesada
                "10": ["11"],            #Fuego Valyrio requiere Piromante
                "8": ["1", "3"]          #Maestre de Guerra requiere infantería y maquinaria
            },
            "exclusion_entre_recursos": {
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
