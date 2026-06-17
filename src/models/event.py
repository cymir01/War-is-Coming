from datetime import datetime

#usar encapsulamiento
class Event:
    def __init__(self, start: datetime, end: datetime, name: str, type: str, location: str, status: str, resources: list = None, description: str = ""):
        self.start = start #date + time
        self.end = end #date + time
        self.name = name
        self.resources = resources or []  #valor por defecto si es None, se trata de los recursos que usa el evento
        self.description = description
        self.status  = status
        self.type = type
        self.location = location

    def get_period(self):
        return [self.start, self.end]
    
    def get_start_date(self):
        return self.start
    
    def get_end_date(self):
        return self.end

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

    @staticmethod
    def from_dict(data):
        """Crea un Event desde diccionario (para cargar desde JSON)"""
        event = Event(
            start=datetime.fromisoformat(data['start']),
            end=datetime.fromisoformat(data['end']),
            name=data['name'],
            resources=data.get('resources', []),
            description=data.get('description', '')
        )
        return event


