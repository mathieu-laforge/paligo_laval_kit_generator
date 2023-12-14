import sqlite3
from datetime import datetime
from utils.file_access import file_access
# datetime object containing current date and time

 


# dd/mm/YY H:M:S


class Last_change_date(str):
    def __init__(self, name: str):
        self.name = name
        
        
    def save_last_modified_date(self):
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        date_db = file_access("db/date", "db")
        connection = sqlite3.connect(date_db)
        cursor = connection.cursor()
        cursor.execute(f'DROP TABLE if exists {self.name}')
        cursor.execute(f'CREATE TABLE if not exists {self.name} (name Text, date_time Text)')
        connection.commit()
        connection.close()
        connection = sqlite3.connect(date_db)
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO {self.name} VALUES (?, ?)',(self.name, date))
        connection.commit()
        connection.close()
        return date