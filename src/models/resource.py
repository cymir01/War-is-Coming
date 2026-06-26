class Resource:
    def __init__(self, id: int, name: str, resource_type: str = None, house: str = None):
        self.id = id
        self.name = name
        self.resource_type = resource_type
        self.house = house
    
    def robject_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "resource_type": self.resource_type,
            "house": self.house
        }
    
    @classmethod
    def create_robject_from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            resource_type=data.get("type"),
            house=data.get("house")
        )
        