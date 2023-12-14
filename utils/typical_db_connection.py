import sqlite3
from utils.file_access import file_access

def typical_db_connection_index(db_relative_path: str, table_name: str, table_index: int):
    split_path = db_relative_path.split(".")
    try:
        file_absolute_path = file_access(split_path[0], split_path[1])
        connection = sqlite3.connect(file_absolute_path)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1")
        zones_validations = cursor.fetchone()
        result = str(zones_validations[table_index])
        connection.close()
        return result
    except Exception as e:
        print(str(e))
        result = "None"
        return result
    
def typical_db_connection(db_relative_path: str, table_name: str, table_index: int):
    split_path = db_relative_path.split(".")
    try:
        file_absolute_path = file_access(split_path[0], split_path[1])
        connection = sqlite3.connect(file_absolute_path)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        zones_validations = cursor.fetchone()
        result = str(zones_validations[table_index])
        connection.close()
        return result
    except Exception as e:
        print(str(e))
        result = "None"
        return result