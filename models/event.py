from datetime import datetime

class Event:
    def __init__(self, start: datetime, end: datetime, era: str,name: str, status: str, resources: list = None, description: str = ""):
        self.start = start
        self.end = end
        self.era = era
        self.name = name
        self.resources = resources or []  #valor por defecto si es None
        self.description = description
        self.status = status

    def get_period(self):
        return [self.start, self.end]

    def get_duration(self):
        return self.end - self.start

    def to_dict(self): #convierte el evento a diccionario para guardar en JSON
        return {
            'name': self.name,
            'description': self.description,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'era': self.era,
            'status': self.status,
            'resources': self.resources,
        }

    @classmethod # https://www.geeksforgeeks.org/python/classmethod-in-python/ explicacion de los class methods
    def from_dict(cls, data):
        """Crea un Event desde diccionario (para cargar desde JSON)"""
        return cls(
            start=datetime.fromisoformat(data['start']),
            end=datetime.fromisoformat(data['end']),
            name=data['name'],
            resources=data.get('resources', []),
            description=data.get('description', '')
        )

start = datetime(2025, 11, 15, 10, 30, 0)
end = datetime(2025, 11, 20, 14, 45, 0)
evento1 = Event(start, end, 'Battle of Winterfell', ['Stark Army', 'Robb Stark'], 'Important battle')

print(evento1.name, evento1.end)