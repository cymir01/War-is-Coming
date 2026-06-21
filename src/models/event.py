from datetime import datetime

#usar encapsulamiento
class Event:
    def __init__(self, id: str, name: str, start: datetime, end: datetime, event_type: str, location: str, resources_ids: list, description: str = "", status: str = "planned"):
        self.id = id
        self.name = name
        self.description = description
        self.start = start
        self.end = end
        self.event_type = event_type
        self.location = location
        self.resources_ids = resources_ids or []  #valor por defecto si es None, se trata de los recursos que usa el evento
        self.status  = status
    
    def __lt__(self, other):
        return self.start < other.start
    
    def get_period(self):
        return [self.start, self.end]
    
    def get_start_date(self):
        return self.start
    
    def get_end_date(self):
        return self.end

    def get_duration(self):
        return self.end - self.start

    def event_to_dict(self): #convierte el evento a diccionario para guardar en JSON
        return {
        "id": self.id,
        'name': self.name,
        'description': self.description,
        'start': self.start.isoformat(),
        'end': self.end.isoformat(),
        'event_type': self.event_type,
        'location': self.location,
        'resources_ids': self.resources_ids,
        'status': self.status
        }

    @classmethod
    def create_event_from_dict(cls, data):
        """Crea un Event desde diccionario (para cargar desde JSON)"""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            start=datetime.fromisoformat(data['start']),
            end=datetime.fromisoformat(data['end']),
            event_type=data['event_type'],
            location=data['location'],
            resources_ids=data['resources_ids'],
            status=data.get('status', 'planned')
        )

