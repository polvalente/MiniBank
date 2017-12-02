import pickle
import psycopg2

class AbstractEventRepository(object):
    def __init__(self, repo_data={}, app_state='last'):
        pass

    def persist_event(self, event):
        raise NotImplementedError
   
    def get_all_events(self, app_state):
        raise NotImplementedError

class InMemoryEventRepository(AbstractEventRepository):
    '''In Memory Event Repository that is able to load from/save to file using Pickle'''
    def __init__(self, repo_data={'filename':''}):
        if repo_data['filename'] == '':
            self.events = []
            self.filename == 'repo.p'
            return self.events

        self.filename = repo_data['filename']
        with open(self.filename, 'rb') as f:
            self.events = pickle.load(f)

    def __del__(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.events, f)

    def persist_event(self, event):
        self.events.append(event)

    def get_all_events(self, last_event_id=None):
        if last_event_id is None:
            return self.events

        return list(filter(lambda e: e.event_id <= app_state, self.events))

class PersistentEventRepository(AbstractEventRepository):
    '''Persistent event repository using PostgresSQL'''
    def __init__(self, repo_data={'dbname:'', address':'', 'port':'', 'user':'', 'pass':''}):
        self.next_event_id = 0
        try:
            self.repo_data = repo_data
            self.connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (repo_data['dbname'], repo_data['user'], repo_data['address'], repo_data['pass'], repo_data['port'])
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            print "Failed to connect to repository %s@%s:%s" % (repo_data['dbname'], repo_data['address'], repo_data['port'])

    def create_table(self):
        create_table_command = "CREATE TABLE IF NOT EXISTS events(id serial PRIMARY KEY, type varchar(30), data jsonb)"
        self.cursor.execute(create_table_command)

        def persist_event(self, event):
            '''persist event into storage'''
        insert_command = "INSERT INTO events(type, data) VALUES('"+event["type"]+"', '"+json.dumps(event["data"])+"')"
        self.cursor.execut(insert_command)

    def get_all_events(self, last_event_id=None):   
        '''Get all events, or if passed 'last_event_id' arg, get all events until specified id'''
        #get all events from database
        self.cursor.execute("SELECT * FROM events")
        events = self.cursor.fetchall()

        #sort events by id
        events = list(sorted(events, key=lambda e: e[0]))
        self.next_event_id = events[-1][0]
        #convert to event objects
        events = list(map(lambda e: Event(e[1], e[2], e[0]), events))

        #check if we need to return all events or only to specified id
        if last_event_id is None:
            #get all events
            return events
        #get events until last_event_id
        return list(filter(lambda e: e.event_id <= last_event_id, events))

    def get_next_id(self):
        self.next_event_id += 1
        return self.next_event_id
