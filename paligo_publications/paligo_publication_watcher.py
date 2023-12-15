import requests

import base64
import time

"""project imports"""
import config as cfg
from concurrent.futures import ThreadPoolExecutor
from utils.file_access import file_access
from utils.app_settings import app_settings
from utils.sqlite_db_management import SqLite_DB_manager
from utils.date import Last_change_date
from utils.sqlite_db_management import SqLite_DB_manager
from paligo_publications.topic_media_object_finder import Topic_media_objects_finder as MF



class Paligo_publication_watcher():
  
    def __init__(self):
        pass
    
    def run_bypass_pub_db(self):
        try: 
            self.selections_list = ["cdu", "autres_regl"]
            self.__PALIGO_CLIENT__ = cfg.paligoConnect["auth"]
            print(self.__PALIGO_CLIENT__)
            self.url = app_settings("prod_paligo_request", "request", "forks")[0][1]
            self.cdu_data_base = file_access("db/paligo", "db")
            self.paligo_db = "db/paligo.db"
            for choice in self.selections_list:
                working_pub_list = []
                publication_list = app_settings("prod_paligo_publications", "publication_category", choice)
                for pub in publication_list:
                    if pub[4] == "publication":
                        working_pub_list.append(pub)
                
                for pub in working_pub_list:
                    self.ordered_forks_fetch_list = []
                    _name = pub[0]
                    _id = pub[1]
                    try:
                        self.paligo_drill_forks_structure([_id], _name)
                    except Exception as e:
                        print("paligo_drilling_structure_error "+ str(e))
                    try:
                        self.save_publication_to_sqlite(self.ordered_forks_fetch_list, _name)
                    except Exception as e:
                        print("failed to save data to sqlite"+str(e))
                    
                    print(f"Traitement de la publication {_name} terminé!")
            generate_date = Last_change_date("all_publications")
            date = generate_date.save_last_modified_date()
            print(date)
            
            #for testing purposes only
            #self.ordered_forks_fetch_list = []
            #self.paligo_drill_forks_structure([25823523], "reglement_l_11870")
            
            
        except Exception as e:
            print("\n"+"Impossible d'effectuer la fonction run_create_publication_database pour la raison suivante: \n" + str(e))
            print("Impossible d'effectuer la fonction run_create_publication_database pour la raison suivante: " + str(e))
        return print("Publication database completed")
        
    def paligo_requests(self, _parent: str):
        """Simple Get Request for Paligo Forks

        Args:
            _parent (_type_): the parent is the publication ID

        Returns:
            _type_: Request obbject
        """        
        apiKey = str(base64.b64encode(self.__PALIGO_CLIENT__.encode('ascii')))
        headers = {
            'Accept': 'application/json',
            'Authorization': "basic" + apiKey,
        }
        params = {
            "parent": str(_parent)
        }
        
        time.sleep(1)
        return requests.get(self.url, headers=headers, params=params)    

    def thread_paligo_requests(self, parent_id_list):
        """Map paligo requests function into a thread

        Args:
            parent_id_list (_type_): a List of items to map into the multi-thread requests

        Returns:
            _type_: a list of al response items return from the request.
        """        

        with ThreadPoolExecutor(max_workers=3) as pool:
            response_list = list(pool.map(self.paligo_requests, parent_id_list))
        all_responses = []

        for response in response_list:
            #print(response.status_code)
            data = response.json()
            all_responses.append(data)

        return all_responses
    
    def paligo_drill_forks_structure(self, publication: list, table_name: str):
        """Descend 5 levels into any Paligo Publication

        Example:
            `self.paligo_drill_forks_structure([1234567], "some_db_name")`
        
        Args:
            publication (list): the publications Ids in a list... Better send only one by one
            name (str): the name of the publication
        """     
           
        print(f"Traitement de la publication... {table_name}")
        depth_1 = self.thread_paligo_requests(publication)
        # self.cdu_folder.append({"titles_folders":get_titles_folders})
        # self.save_data_to_sqlite(self.cdu_folder)
        print("clé = " + self.__PALIGO_CLIENT__)
        print(depth_1)
        for i in depth_1:
            depth_1_response = i["forks"]
            depth_1_id_list = []
            for f in depth_1_response:
                print(f["document"]["name"])
                fork_id = f["id"]
                fork_uuid = f["uuid"]
                _parent = f["parent"]
                _position = f["position"]
                _depth = f["depth"]
                doc_id = f["document"]["id"]
                doc_name = f["document"]["name"]
                doc_content = f["document"]["content"]
                doc_taxonomy = f["document"]["taxonomies"]
                
                depth_1_id_list.append(fork_id)
                depth_1_name = f["document"]["name"]
                #print("extracting {}".format(f["document"]["name"]))
                if f["document"]["name"] != "Grilles de zonage":
                    self.ordered_forks_fetch_list.append({"id": fork_id,"uuid": fork_uuid, "parent": _parent, "position": _position, "depth": _depth, "document": {"id": doc_id, "name": doc_name,"taxonomies": doc_taxonomy, "content": doc_content}})
            if fork_id:    
                depth_2 = self.thread_paligo_requests(depth_1_id_list)
            
                for i in depth_2:
                    depth_2_response = i["forks"]
                    depth_2_id_list = []
                    for f in depth_2_response:
                      
                        print(f["document"]["name"])
                        fork_id = f["id"]
                        fork_uuid = f["uuid"]
                        _parent = f["parent"]
                        _position = f["position"]
                        _depth = f["depth"]
                        doc_id = f["document"]["id"]
                        doc_name = f["document"]["name"]
                        doc_content = f["document"]["content"]
                        doc_taxonomy = f["document"]["taxonomies"]
                    
                        depth_2_id_list.append(fork_id)
                        #print("extracting {}".format(f["document"]["name"]))
                        if f["document"]["name"] != "Grilles de zonage":
                            self.ordered_forks_fetch_list.append({"id": fork_id,"uuid": fork_uuid, "parent": _parent, "position": _position, "depth": _depth, "document": {"id": doc_id, "name": doc_name,"taxonomies": doc_taxonomy, "content": doc_content}})
                    if fork_id:    
                        depth_3 = self.thread_paligo_requests(depth_2_id_list)
                        
                        for i in depth_3:
                            depth_3_response = i["forks"]
                            depth_3_id_list = []
                            for f in depth_3_response:
                                
                                print(f["document"]["name"])
                                fork_id = f["id"]
                                fork_uuid = f["uuid"]
                                _parent = f["parent"]
                                _position = f["position"]
                                _depth = f["depth"]
                                doc_id = f["document"]["id"]
                                doc_name = f["document"]["name"]
                                doc_content = f["document"]["content"]
                                doc_taxonomy = f["document"]["taxonomies"]
                                depth_3_id_list.append(fork_id)
                                #print("extracting {}".format(f["document"]["name"]))
                                self.ordered_forks_fetch_list.append({"id": fork_id,"uuid": fork_uuid, "parent": _parent, "position": _position, "depth": _depth, "document": {"id": doc_id, "name": doc_name,"taxonomies": doc_taxonomy, "content": doc_content}})
                            if fork_id:
                                depth_4 = self.thread_paligo_requests(depth_3_id_list)
                                
                                for i in depth_4:
                                    depth_4_response = i["forks"]
                                    depth_4_id_list = []
                                    for f in depth_4_response:
                                        print(f["document"]["name"])
                                       
                                        fork_id = f["id"]
                                        fork_uuid = f["uuid"]
                                        _parent = f["parent"]
                                        _position = f["position"]
                                        _depth = f["depth"]
                                        doc_id = f["document"]["id"]
                                        doc_name = f["document"]["name"]
                                        doc_content = f["document"]["content"]
                                        doc_taxonomy = f["document"]["taxonomies"]
                                        depth_4_id_list.append(fork_id)
                                        #print("extracting {}".format(f["document"]["name"]))
                                        self.ordered_forks_fetch_list.append({"id": fork_id,"uuid": fork_uuid, "parent": _parent, "position": _position, "depth": _depth, "document": {"id": doc_id, "name": doc_name,"taxonomies": doc_taxonomy, "content": doc_content}})
                                    if fork_id:    
                                        depth_5 = self.thread_paligo_requests(depth_4_id_list)
                                        
                                        for i in depth_5:
                                            depth_5_response = i["forks"]
                                            depth_5_id_list = []
                                            for f in depth_5_response:
                                                print(f["document"]["name"])
                                                fork_id = f["id"]
                                                fork_uuid = f["uuid"]
                                                _parent = f["parent"]
                                                _position = f["position"]
                                                _depth = f["depth"]
                                                doc_id = f["document"]["id"]
                                                doc_name = f["document"]["name"]
                                                doc_content = f["document"]["content"]
                                                doc_taxonomy = f["document"]["taxonomies"]
                                                depth_5_id_list.append(fork_id)
                                                #print("extracting {}".format(f["document"]["name"]))
                                                self.ordered_forks_fetch_list.append({"id": fork_id,"uuid": fork_uuid, "parent": _parent, "position": _position, "depth": _depth, "document": {"id": doc_id, "name": doc_name,"taxonomies": doc_taxonomy, "content": doc_content}})
                                                
                                                
                                            if fork_id:    
                                                depth_6 = self.thread_paligo_requests(depth_5_id_list)

                                                for i in depth_6:
                                                    depth_6_response = i["forks"]
                                                    depth_6_id_list = []
                                                    for f in depth_6_response:
                                                        print(f["document"]["name"])
                                                        fork_id = f["id"]
                                                        fork_uuid = f["uuid"]
                                                        _parent = f["parent"]
                                                        _position = f["position"]
                                                        _depth = f["depth"]
                                                        doc_id = f["document"]["id"]
                                                        doc_name = f["document"]["name"]
                                                        doc_content = f["document"]["content"]
                                                        doc_taxonomy = f["document"]["taxonomies"]
                                                        depth_6_id_list.append(fork_id)
                                                        #print("extracting {}".format(f["document"]["name"]))
                                                        self.ordered_forks_fetch_list.append({"id": fork_id,"uuid": fork_uuid, "parent": _parent, "position": _position, "depth": _depth, "document": {"id": doc_id, "name": doc_name, "taxonomies": doc_taxonomy, "content": doc_content}})
                                                        
                                                        
        #print(self.ordered_forks_fetch_list)
        return self.ordered_forks_fetch_list                                                
        
        
        
    def save_publication_to_sqlite(self, input_data: list, table_name: str):
        """Save All collected Data from requests into SQlite Table in the predefined database

        Args:
            input_data (list): List of all topics collected from requests
            table_name (str): Name of the table to save the data
        """ 
        self.publications_db = SqLite_DB_manager(self.paligo_db, table_name) 
        self.publications_db.create_table(["fork_id Int", "uuid Text", "parent Text", "position Text", "depth Text", "doc_id Text", "doc_name Text", "doc_taxonomies Text", "doc_content Text", "num_figures Int", "figures_data Text"], "fork_id")      
        """connection = sqlite3.connect(self.cdu_data_base)
        cursor = connection.cursor()
        try:
            cursor.execute(f'DROP TABLE if exists {table_name}')
        except Exception as e:
            print(e)
            
        cursor.execute(
            f'CREATE TABLE if not exists {table_name} (id Int, uuid Text, parent Text, position Text, depth Text, doc_id Text, doc_name Text, doc_taxonomies Text, doc_content Text, num_figures Int, figures_data Text)')
        connection.commit()"""
        display_DB = SqLite_DB_manager("db/display_paligo.db", table_name)
        display_DB.create_table(["fork_id Int", "topic_id Int", "name Text", "taxonomies Text", "num_figures Int", "figures_data Text"], "fork_id")
        for topic in input_data:
            
            
            if "id" in topic:
                _id = topic["id"]
            else:
                _id = None
            
            if "uuid" in topic:
                _uuid = topic["uuid"]
            else:
                _uuid = None
            
            if "parent" in topic:
                _parent = topic["parent"]
            else:
                _parent = None
                
            if "position" in topic:
                _position = topic["position"]
            else:
                _position = None
                
            if "depth" in topic:
                _depth = topic["depth"]
            else:
                _depth = None
                
            if "id" in topic["document"]:
                _doc_id = topic["document"]["id"]
            else:
                _doc_id = None
            
            if "name" in topic["document"]:
                _doc_name = topic["document"]["name"]
            else:
                _doc_name = None
            
            if "taxonomies" in topic["document"]:
                taxonomies = topic["document"]["taxonomies"]
                taxonomies_list = []
                for tax in taxonomies:
                    tax_name = tax["title"]
                    taxonomies_list.append(tax_name)
                _doc_taxonomies = ", ".join(taxonomies_list)
            else:
                _doc_taxonomies = None
            
            if "content" in topic["document"]:
                _doc_content = topic["document"]["content"]
            else:
                _doc_content = None
            images_list = MF().media_objects_finder(_doc_content)
            _num_figures = len(images_list)     
            images_data = []
            for image in images_list:
                image_strings = str(image)
                images_data.append(image_strings)
            _figures_data = ", ".join(images_data)

            
            display_DB.insert_or_replace_data(["fork_id","topic_id", "name", "taxonomies", "num_figures", "figures_data"], (_id, _doc_id, _doc_name, _doc_taxonomies, _num_figures, _figures_data))
            self.publications_db.insert_or_replace_data(["fork_id", "uuid", "parent", "position", "depth", "doc_id", "doc_name", "doc_taxonomies", "doc_content", "num_figures", "figures_data"], (_id, _uuid, _parent, _position, _depth, _doc_id, _doc_name,  _doc_taxonomies, _doc_content, _num_figures, _figures_data))
            """cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?,?,?,?,?,?,?)', (_id, _uuid, _parent, _position, _depth, _doc_id, _doc_name,  _doc_taxonomies, _doc_content, _num_figures, _figures_data))
            connection.commit()"""
            print(f"Data added in table: {table_name} - {_doc_name}")
        #connection.close()
        
if __name__ == "__main__":
    watcher = Paligo_publication_watcher()
    watcher.run_bypass_pub_db()
    