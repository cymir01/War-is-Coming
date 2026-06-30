from datetime import datetime

#AGREGAR EL ATRIBUTO ERA (AC, DC) PARA IMPRIMIR SOLO
#usar encapsulamiento
class Event:
    """Representa un evento planificable en el sistema. 
    Un evento tiene un identificador único, nombre, fechas de inicio y fin, 
    tipo, ubicación opcional, lista de recursos asignados, estado y era histórica
    """
    def __init__(self, id: str, name: str, start: datetime, end: datetime, event_type: str, location: str = None, resources_ids: list = [], description: str = None, status: str = "planned", era: str = "DC"):
        """
        Inicializa un nuevo evento.
        Args:
        id (str): Identificador único del evento
        name (str): Nombre del evento
        start (datetime): Fecha y hora de inicio
        end (datetime): Fecha y hora de fin
        event_type (str): Tipo de evento (Asedio, Batalla naval, etc)
        location (str): Ubicación del evento. Valor por defecto: None
        resources_ids (list): IDs de recursos asignados. Valor por defecto: []
        description (str): Descripción del evento. Valor por defecto: None
        status (str): Estado del evento. Valor por defecto: "planned"
        era (str): Era histórica (DC o AC). Valor por defecto: "DC"
        """
        self.id = id
        self.name = name
        self.description = description
        self.start = start
        self.end = end
        self.event_type = event_type
        self.location = location
        self.resources_ids = resources_ids
        self.status  = status
        self.era = era
    
    def __lt__(self, other):
        """
        Compara dos eventos por fecha de inicio.
        Permite ordenar eventos cronológicamente con sort() y bisect.
        Args:
        other (Event): Otro evento con el que comparar
        Returns:
        bool: True si este evento comienza antes que el otro
        """
        return self.start < other.start
    
    def get_period(self):
        """
        Obtiene el periodo de tiempo del evento.
        Returns:
        list: [start, end] Lista con las fechas de inicio y fin
        """
        return [self.start, self.end]
    
    def get_start_date(self):
        """Obtiene la fecha de inicio del evento.
        Returns:
        datetime: Fecha y hora de inicio
        """
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
        'status': self.status,
        'era': self.era
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
            status=data.get('status', 'planned'),
            era=data.get('era', "DC")
        )

