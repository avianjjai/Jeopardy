import pandas as pd

class Table:
    def __init__(self, columns) -> None:
        self.columns = columns
        self.df = pd.DataFrame({key: [] for key in self.columns})

    def insertSingleRecord(self, record):
        self.df.loc[len(self.df.index)] = list(record)

    def insertAllRecords(self, records):
        for record in records:
            self.insertSingleRecord(record)

    def getTable(self):
        return self.df