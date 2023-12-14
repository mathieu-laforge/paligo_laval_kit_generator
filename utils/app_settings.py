import sqlite3
from utils.file_access import file_access

def app_settings(table_name:str, column_name: str, setting: str):
    """Query Application Settings database. Returns the core data to make the application Work

    Example: 
        table_name = "prod_paligo_request", "prod_cdu_folders", "prod_ceg_requests", "prod_grids", "prod_paligo_tags", "prod_paligo_token", "prod_rules_and_masters"

    Args:
        table_name (str): the table name in the app_settings.db
        column_name (str): column header name of the chosen table
        setting (str): the value to look up in the table

    Returns:
        list: The result of the app settings database query
    """    
    app_settings_db = file_access("db/app_settings", "db")
    connection = sqlite3.connect(app_settings_db)
    cursor = connection.cursor()
    setting_query = cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} LIKE '%{setting}%'")
    result = setting_query.fetchall()
    connection.close()
    return result
