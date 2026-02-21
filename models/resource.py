class Resource:
    def __init__(self, name, id, type, house, total_amount, available_amount, status, attributes):
        self.name = name
        self.id = id
        self.type = type
        self.house = house
        self.total_amount = total_amount
        self.available_amount = available_amount
        self.attributes = attributes #!esto tendria {movilidad, rendimiento}
        self.status = status

    def to_dict(self) -> dict:
        """convierte el recurso a un diccionario para json"""
        return {
            "name": self.name,
            "resource_type": self.resource_type,
            "house": self.house,
            "total_amount": self.total_amount,
            "available_amount": self.available_amount,
            "attributes": self.attributes,
            "description": self.description,
            "status": self.status
        }

    # def get_resource():