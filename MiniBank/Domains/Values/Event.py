class Event(object):
    def __init__(self, event_type, event_value, event_id):
        '''event_type is a string according to the '__call__' method (e.g: 'event()')
        event_value is a dictionary containing each event's attributes'''
            
        self.etype = event_type
        self.value = event_value
        self.event_id = event_id
