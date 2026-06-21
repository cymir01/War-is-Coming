class Resource:
    def __init__(self, id: int, name: str, house: str = ""):
        self.id == id
        self.name == name
        self.house == house
    
    def robject_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "house": self.name
        }
    
    @classmethod
    def create_robject_from_dict(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            house=data.get("house", "")
        )
        