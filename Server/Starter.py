from PersistentStorage import PersistentStorage

election_database_attr = dict(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'election'
)

persistanceStorage = PersistentStorage(**election_database_attr)
query = 'select * from constituency'
table = persistanceStorage.executeQuery(query)

for record in table:
    print(record)