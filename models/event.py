from datetime import datetime

class Event:
    def __init__(self, start: datetime, end: datetime, name: str, resources: list = None, description: str = ""):
        """
        Constructor corregido - los parámetros deben coincidir con la instanciación
        """
        self.start = start
        self.end = end
        self.name = name
        self.resources = resources or []  # Valor por defecto si es None
        self.description = description

    def get_period(self):
        """Retorna el período completo del evento"""
        return [self.start, self.end]  # ✅ CORREGIDO: [start, end]

    def get_duration(self):
        """Calcula la duración del evento"""
        return self.end - self.start

    def get_duration_hours(self):
        """Duración en horas"""
        duration = self.get_duration()
        return duration.total_seconds() / 3600

    def to_dict(self):
        """Convierte el evento a diccionario para guardar en JSON"""
        return {
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'name': self.name,
            'resources': self.resources,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un Event desde diccionario (para cargar desde JSON)"""
        return cls(
            start=datetime.fromisoformat(data['start']),
            end=datetime.fromisoformat(data['end']),
            name=data['name'],
            resources=data.get('resources', []),
            description=data.get('description', '')
        )

# ✅ INSTANCIACIÓN CORRECTA:
start = datetime(2025, 11, 15, 10, 30, 0)  # ✅ Sin datetime.datetime
end = datetime(2025, 11, 20, 14, 45, 0)
evento1 = Event(start, end, 'Battle of Winterfell', ['Stark Army', 'Robb Stark'], 'Important battle')  # ✅ Parámetros correctos

print(evento1.name)  # ✅ Funciona
print(f"Duración: {evento1.get_duration_hours():.1f} horas")  # ✅ Nuevo método