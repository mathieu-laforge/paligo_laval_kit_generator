import sqlite3
from utils.file_access import file_access

table_headers_list = ["name Text", "html Text"]


class SqLite_DB_manager:
    """Function to manage SQLite database CRUD operations
    
    Arguments
    ---------
    :db_name_path: (string)
        The relative path to the SQlite database existant or new. WITH THE FILE EXTENSION ex: .db
    :table_name: (string)
        The name of the table to do CRUD operations    
    """
    def __init__(self, db_name_path: str, table_name: str):
        self.db_name_path = db_name_path
        split_name = db_name_path.split(".")
        self.file_name = file_access(split_name[0], split_name[1])
        self.table_name = table_name
        
    def create_table(self, table_headers_list: list, index_column_name: str, index= False, keep_table = False):
        """Create a SQlite DB and table

        Args:
            table_headers_list (list): a list of your table param like: [ "id Int", "name Text", etc. ]
            index_column_name (str): Specify the column name to create a self-numbering index from
            
        `index_column_name` allow you to choose the reference column for `REPLACE` or `INSERT` sqlite queries.
        """
        try:
            self.headers = ", ".join(table_headers_list)
            connection = sqlite3.connect(self.file_name)
            cursor = connection.cursor()
            if keep_table == False:
                cursor.execute(f'DROP TABLE if exists {self.table_name}')
            cursor.execute(f'CREATE TABLE if not exists {self.table_name} (id INTEGER PRIMARY KEY, {self.headers})')
        except:
            print("this db already Exist in the defined path")
            connection.close()
        finally:
            if index == True:   
                cursor.execute(f'CREATE UNIQUE INDEX IF NOT EXISTS idx_{self.table_name} ON {self.table_name} ({index_column_name})')
                print(f"Table {self.table_name} créée dans {self.db_name_path} avec succès")
                connection.commit()
                connection.close()
    
    def insert_or_replace_data(self, column_names: list,  table_data: tuple):
        """_summary_

        Args:
            column_names (list): list of the columns in your table by order as created
            table_data (tuple): a tuple of the data to insert in the table
        """
        try:
            self.column_names = ", ".join(column_names)
            data_lenght = len(table_data)
            number_of_columns = str(", ".join(data_lenght*"?"))
            connection = sqlite3.connect(self.file_name)
            cursor = connection.cursor()
            cursor.execute(f'REPLACE INTO {self.table_name}({self.column_names}) VALUES ({number_of_columns})',
                        (table_data))
            print(f"Insertion de données avec succès dans la {self.table_name}")
            connection.commit()
            connection.close()
        except Exception as e:
            print("Erreur lors de l'insertion de données "+str(e))
    
    def delete_by_id(self, id:str, column_name:str):
        try:
            connection = sqlite3.connect(self.file_name)
            sql = f"DELETE FROM {self.table_name} WHERE {column_name}=?"
            cur = connection.cursor()
            cur.execute(sql, (id,))
            connection.commit()
        except Exception as e:
            print("Erreur lors de la requête "+str(e))       
    
    def fetch_all_data(self, parameters = "", fetchAll = True):
        """Fetch Data from a DB

        Args:
            parameters (str, optional): Indicate all query parameters after specifying the table name. Defaults to "".
            fetchAll (bool, optional): Indicate False to fetchOne result from query. Defaults to True for fetchAll

        Returns:
            data (list): List of tuple from the query parameters
        """        
        try:
            connection = sqlite3.connect(self.file_name)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} {parameters}")
            if fetchAll == True:
                data = cursor.fetchall()
                connection.close()
                return data
            else:
                data = cursor.fetchone()
                connection.close()
                return data
        except Exception as e:
            print("Erreur lors de la requête "+str(e))
            
        """CREATE NEW QUERY TO UPDATE ANY SQLITE TABLE ROW AFTER POST.
        """
        
    def update_data(self, sql_query_set: str, column_name_reference: str ,updated_data:tuple):
        try:
            connection = sqlite3.connect(self.file_name)
            cursor = connection.cursor()
            sql = f"""UPDATE {self.table_name} SET {sql_query_set} WHERE {column_name_reference} = ?"""
            cursor.execute(sql, updated_data)
            connection.commit()
            print("Sqlite Table updated!")
        except Exception as e:
            print("Erreur lors de la requête "+str(e))
            
    def list_all_tables(self):
        try:
            
            # Making a connection between sqlite3 
            # database and Python Program
            sqliteConnection = sqlite3.connect(self.file_name)
            
            # If sqlite3 makes a connection with python
            # program then it will print "Connected to SQLite"
            # Otherwise it will show errors
            #print("Connected to SQLite")
        
            # Getting all tables from sqlite_master
            sql_query = """SELECT name FROM sqlite_master 
            WHERE type='table';"""
        
            # Creating cursor object using connection object
            cursor = sqliteConnection.cursor()
            
            # executing our sql query
            cursor.execute(sql_query)
            #print("List of tables\n")
            
            # printing all tables list
            return cursor.fetchall()
        
        except sqlite3.Error as error:
            print("Failed to execute the above query", error)
            
        finally:
        
            # Inside Finally Block, If connection is
            # open, we need to close it
            if sqliteConnection:
                
                # using close() method, we will close 
                # the connection
                sqliteConnection.close()
                
                # After closing connection object, we 
                # will print "the sqlite connection is 
                # closed"
                #print("the sqlite connection is closed")