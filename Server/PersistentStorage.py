import mysql.connector as connector

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

    def executeQuery(self, query):
        cursor = self.cursor.execute(query)
        table = self.cursor.fetchall()
        return table

        