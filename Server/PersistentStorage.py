import mysql.connector as connector
from Table import Table

class PersistentStorage:
    def __init__(self, host, user, password, database) -> None:
        self.connection_attr = dict(
            host = host,
            user = user,
            password = password,
            database = database
        )

        self.connection = connector.connect(**self.connection_attr)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def executeQuery(self, columns, tableName, condition='True'):
        query = "SELECT " + ','.join(columns) + " FROM " + tableName + " WHERE " + condition
        self.cursor.execute(query)

        columns = [c[0] for c in self.cursor.description]
        table = Table(columns)
        
        records = self.cursor.fetchall()
        table.insertAllRecords(records)
        
        return table