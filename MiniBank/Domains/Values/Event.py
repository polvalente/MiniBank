class Event(object):
    def __init__(self, event_type, event_value, event_id):
        '''event_type is a string according to the '__call__' method (e.g: 'event()')
        event_value is a dictionary containing each event's attributes'''
            
        self.etype = event_type
        self.value = event_value
        self.event_id = event_id

    def __eq__(self, other):
        return self.etype == other.etype and self.value == other.value and self.event_id == other.event_id

    def __iter__(self):
        yield 'type', self.etype
        yield 'value', self.value
        yield 'event_id', self.event_id
