import threading

SERVER_IDENTITY = dict(
    IP = '',
    PORT = 3000
)

lock = threading.Lock()

election_database_attribute = dict(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'election'
)

sport_database_attribute = dict(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'Sports'
)

technology_database_attribute = dict(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'Technology'
)