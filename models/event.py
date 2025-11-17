import datetime

class Event:

    def __init__(self, start: datetime, end: datetime, resources, name, description):
        self.start = start
        self.end = end
        self.resources = resources
        self.name = name
        self.description = description

    def get_period(self):
        return [self.,]

