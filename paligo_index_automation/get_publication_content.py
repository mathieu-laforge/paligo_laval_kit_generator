from utils.sqlite_db_management import SqLite_DB_manager

class Publication_content:
    def __init__(self, publication_table_name):
        """_summary_

        Args:
            publication_table_name (_type_): autres_règlements, cdu_publication ou warnings
        """        
        self.publication_table_name = publication_table_name
        
        
    def get_sql_DB(self):
        sql_db = SqLite_DB_manager("db/paligo.db", self.publication_table_name)
        pub_content = sql_db.fetch_all_data()
        return pub_content
# id = 0
# doc_id = 6
# doc_content = 9       
        
if __name__ == "__main__":
    pub_content = Publication_content("cdu_publication")
    