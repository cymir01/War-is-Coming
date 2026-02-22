class Resource:
    def __init__(self, name, id, type, house, total_amount, available_amount, status, attributes=None, description=""):
        self.name = name
        self.id = id
        self.type = type
        self.house = house
        self.total_amount = total_amount
        self.available_amount = available_amount
        self.attributes = attributes or {}
        self.status = status
        self.description = description

    def __str__(self):
        return f"{self.name} (Casa {self.house}) - {self.available_amount}/{self.total_amount} disponible"

    def __repr__(self):
        return f"Resource(name='{self.name}', house='{self.house}', type='{self.type}')"

    def to_dict(self) -> dict:
        """Convierte el recurso a un diccionario para JSON"""
        return {
            "name": self.name,
            "id": self.id,
            "type": self.type,
            "house": self.house,
            "total_amount": self.total_amount,
            "available_amount": self.available_amount,
            "attributes": self.attributes,
            "status": self.status,
            "description": self.description
        }

    @staticmethod
    def from_dict(data):
        """Crea un Resource desde diccionario (para cargar desde JSON)"""
        return Resource(
            name=data['name'],
            id=data.get('id', 0),  # El ID real vendrá de la clave del dict en core.py
            type=data['type'],
            house=data['house'],
            total_amount=data['total_amount'],
            available_amount=data['available_amount'],
            status=data['status'],
            attributes=data.get('attributes', {}),
            description=data.get('description', '')
        )

    def is_available(self, amount_needed=1):
        """Verifica si hay suficientes unidades disponibles"""
        return self.available_amount >= amount_needed

    def use_resource(self, amount=1):
        """Usa una cantidad del recurso"""
        if self.is_available(amount):
            self.available_amount -= amount
            if self.available_amount == 0:
                self.status = "agotado"
            return True
        return False

    def release_resource(self, amount=1):
        """Libera una cantidad del recurso"""
        self.available_amount = min(self.total_amount, self.available_amount + amount)
        if self.available_amount > 0:
            self.status = "disponible"
        return True

    def belongs_to_house(self, house_name):
        """Verifica si el recurso pertenece a una casa específica"""
        return self.house.lower() == house_name.lower()

    def is_of_type(self, resource_type):
        """Verifica si el recurso es de un tipo específico"""
        return self.type.lower() == resource_type.lower()