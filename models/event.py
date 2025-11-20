import datetime

class Event:

    def __init__(self, start: datetime, end: datetime, resources, name, description):
        self.start = start
        self.end = end
        self.resources = resources
        self.name = name
        self.description = description

    def get_period(self):
        return [self.start, self.start]

start = datetime.datetime(2025, 11, 15, 10, 30, 0) 
end = datetime.datetime(2025, 11, 20, 14, 45, 0) 
evento1 = Event(start, end, 'Battle', 'bla bla')
print(evento1.name)