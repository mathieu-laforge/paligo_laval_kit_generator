from paligo_requests.paligo_requests import Paligo_request
from utils.app_settings import app_settings
from generate_pdf_kits.data_preparation import tag_list_for_kits, get_paligo_content_by_tag, tag_replacements_names
import time

# type: publication article
# subtype: -



class Generate_kits_publications:
    def __init__(self):
        # get rules table
        self.document_url = app_settings("prod_paligo_request", "request", "document")[0][1]
        self.kits_folder_id = 40199837
        self.paligo_request = Paligo_request("prod")
        self.kit_lists = tag_list_for_kits()
        self.kit_lists_names = []
        for name in self.kit_lists:
            self.kit_lists_names.append(name["title"])
        self.existing_publications = self.fetch_existing_publications()
        self.pub_list_names = []
        for name in self.existing_publications:
            self.pub_list_names.append(name["name"])
    
    def run_kits_generator(self):
        try:
            self.delete_intruder_publications()
        except Exception as e:
            print("Error with delete function")
            print(e)
        try:
            self.create_new_kit()
        except Exception as e:
            print("Error with create function")
            print(e)
        try:
            self.run_kit_update()
        except Exception as e:
            print("Error with update function")
            print(e)

        
    def fetch_existing_publications(self):
        publications = self.paligo_request.paligo_list_generator(self.document_url, self.kits_folder_id)
        all_documents = []
        for p in publications:
            for d in p["documents"]:
                all_documents.append(d)
        #print(all_documents)
        return all_documents
    
    def create_new_kit(self):
        new_publications = [x for x in self.kit_lists if x["title"] not in self.pub_list_names]
        #print(new_publications)
        if len(new_publications) == 0:
            print("0 publication to create.")  
        
        for topic_data in new_publications:
            topic_name = topic_data["title"]
            names_list = tag_replacements_names()
            name = [x["displayName"] for x in names_list if x["tag"] == topic_data["title"]]
            if len(name) == 0:
                print(f"The creation of: {topic_name} is impossible!")
                print("Verify if the tag is listed in the Dashboard")
            else:
                topic_title = name[0]
                self.create_publications_topics(topic_data, topic_title)
        
    def delete_intruder_publications(self):
        intruders = [x for x in self.existing_publications if x["name"] not in self.kit_lists_names]
        #print(intruders)
        if len(intruders) == 0:
            print("0 intruder was found in the folder KITS DE RÈGLEMENTS.")
        else:
            print(f"{str(len(intruders))} intruder(s) was found in the folder KITS DE RÈGLEMENTS.")
            for i in intruders:
                name = i["name"]
                response = self.paligo_request.delete_paligo_forks(self.document_url, i["id"])
                print(f"Delete topic: {name}")
                print(response)
             
    def create_publications_topics(self, topic_data, topic_title):
        topic_name = topic_data["title"]
        basic_publication_content = f"""<?xml version="1.0"?>
        <article xmlns="http://docbook.org/ns/docbook" xmlns:xinfo="http://ns.expertinfo.se/cms/xmlns/1.0">
        <info>
            <title>{topic_title}</title>
            <subtitle></subtitle>
            <mediaobject role="titleimage">
            <imageobject>
                <imagedata/>
            </imageobject>
            </mediaobject>
            <volumenum xinfo:translate="no"><?placeholder Publication ID?></volumenum>
            <pubdate xinfo:translate="no"><?placeholder Publication date?></pubdate>
            <copyright xinfo:translate="no">
            <year><?placeholder Year ?></year>
            <holder><?placeholder Holder?></holder>
            </copyright>
            <legalnotice xinfo:translate="no">
            <para><?placeholder Legal notice text?></para>
            </legalnotice>
            <abstract>
            <para><?placeholder Abstract text?></para>
            </abstract>
        </info>
        </article>"""

        print(f"Creating publication: {topic_name}")
        response = self.paligo_request.paligo_create_document(self.document_url, self.kits_folder_id, topic_name, basic_publication_content, "publication")
        print(response.status_code)
        time.sleep(3)
    
    def run_kit_update(self):
        publications = self.fetch_existing_publications()
        for pub_data in publications:
            Update_kit_publication(pub_data)
            

class Update_kit_publication:
    def __init__(self, publication_data):
        # State requests informations
        self.paligo_r = Paligo_request("prod")
        self.forks_url = app_settings("prod_paligo_request", "request", "forks")[0][1]
        
        # Init publication data input
        self.publication_data = publication_data
        
        # Match db articles with the tag name
        self.matched_articles = get_paligo_content_by_tag(self.publication_data["name"])
        # Fetch the publication content
        self.pub_content = self.fetch_publication_content()
        # Find intruder articles in the publication content
        self.intruders = self.find_intruders_articles()
        if self.intruders is not None:
            # Remove intruders from publication
            self.delete_forks(self.intruders)
            # Fetch the publication content
            self.pub_content = self.fetch_publication_content()
        # Verify organization and order
        self.update_publication_kits()
          
        
        
        
        
        
    def fetch_publication_content(self):
        return self.paligo_r.get_list_of_documents_by_params(self.forks_url, self.publication_data["id"])
    
    def update_publication_kits(self):
        pub_name = self.publication_data["name"]
        existing_articles = [x["document"]["name"] for x in self.pub_content["forks"]]
        deletion_list = [x for x in self.pub_content["forks"]]
        new_articles = [x[7] for x in self.matched_articles]
        if existing_articles == new_articles:
            print(f"{pub_name} is OK")
            pass
        else:
            if len(deletion_list) != 0:
                self.delete_forks(deletion_list)
            
            for i, x in enumerate(self.matched_articles):
                
                _id = x[1]
                _name = x[7]
                _position = i+1
                self.paligo_r.post_publications_forks_with_order(self.forks_url, _id, self.publication_data["id"], _position)
                time.sleep(3)
                print(f"Ajout du topic {_name} à la publication {pub_name}")
            print(f"{pub_name} is completed")
        
    def find_missing_content(self):
        pass
    
    def find_intruders_articles(self):
        if len(self.pub_content["forks"]) != 0: 
            intruders = [x for x in self.pub_content["forks"] if x["document"]["name"] not in [x[7] for x in self.matched_articles]]
            return intruders
        else:
            return None
            
    
    
    def delete_forks(self, deletion_list:list):
        """Delete intruders in girds
        
        ex:
            self.delete_intruders(["id": "123456789", "name": "1000", "fork_id": "123456789"])

        Args:
            intruders_list (list): a list of the intruders to delete

        Raises:
            Exception: if a 204, it's a fail
        """        
        for i in deletion_list:
            fork_id = i["id"]
            if "document" not in i:
                name = i["name"]
            else:
                name = i["document"]["name"]
        
            del_response = self.paligo_r.delete_paligo_forks(self.forks_url, fork_id)
            if del_response != 204:
                raise Exception("Delete request failed")
            print(f"Le topic {name} a été supprimé de la publication.")    
            time.sleep(3)
            
if __name__ == "__main__":
    gen_kit = Generate_kits_publications()
    gen_kit.run_kits_generator()
    #gen_kit.run_kit_update()