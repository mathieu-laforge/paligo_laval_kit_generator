from utils.file_access import file_access
from utils.sqlite_db_management import SqLite_DB_manager
from utils.json_files import read_data_from_json, save_data_to_json
from bs4 import BeautifulSoup as Soup
from paligo_requests.paligo_requests import Paligo_request
import os
import time
 



class Find_topic_versions():
    """Analyse and structure topic data for reverting versions
    """
    parsed_Topic_v1 = 0
    parsed_Topic_v2 = 0
    def __init__(self):
        self.paligo_r = Paligo_request("prod")
        self.missed_revert_articles = []
        data = read_data_from_json("paligo_rebuild_versionning\\temprestart_list_v2.json")
        self.restart_list = data
    def collect_versionning_data(self):
        # Make sys path
        v1_publication_xml_file = file_access("db\cdu_xml", "xml")
        list_of_versioned_articles_json = file_access("db\liste_articles_versionnés", "json")
        # fetch sqlite cdu db
        sqlite_con = SqLite_DB_manager("db\paligo.db", "cdu_publication")
        v2_paligo_db = sqlite_con.fetch_all_data()
        
        #read json file
        list_of_versioned_articles = read_data_from_json(list_of_versioned_articles_json)
        
        #read xml file
        with open(v1_publication_xml_file, 'r', encoding="utf8") as f:
            v1_publication_xml = f.read()
        #Uniformize data
        v1_publication_parsed = self.xml_string_v1(v1_publication_xml)
        v2_paligo_db_parsed = self.xml_string_v2(v2_paligo_db)
        filtered_data_base = self.filtering_data(list_of_versioned_articles, v1_publication_parsed, v2_paligo_db_parsed)
        save_data_to_json(filtered_data_base, "list_articles_for_reverting.json")
        
        
        return filtered_data_base
    
    def filtering_data(self, list_of_versioned_articles: list, v1, v2):
        """#
        Args:
            list_of_versioned_articles (_type_): list of versionned articles
        
        """
        error_list = []
        reverting_articles_list = []
        ### A FAIRE tester si le match est len = 0 faut lever un flag
        for i in list_of_versioned_articles:
            ressource_title = str(i["reference"]).split("/")[-1].strip()
            
            match_in_v1 = [x for x in v1 if x["attributes"]["xinfo:resource-title"].lower().split(" ")[0].startswith(ressource_title.lower().split(" ")[0])]
            match_in_v2 = [x for x in v2 if x["attributes"]["xinfo:resource-title"].lower().split(" ")[0].startswith(ressource_title.lower().split(" ")[0])]
            if len(match_in_v1) == 0 or len(match_in_v2) == 0:
                error_list.append({"no_match_found": ressource_title})
            
            if len(match_in_v1) != 0 and len(match_in_v2) != 0:
                reverting_articles_list.append({"v1": match_in_v1[0], "v2": match_in_v2[0]})
        save_data_to_json(error_list, "match_error_list.json")
        save_data_to_json(reverting_articles_list, "reverting_articles_list.json")
        return reverting_articles_list
        
        
    def xml_string_v1(self, publication_xml, v1: bool = True):      
        """For xml publication file from Paligo - index.xml 
        Args:
            publication_xml (_type_): the xml file in html5 publication from Paligo

        Returns:
            list: of stuf like this {'content': '\n<title>\n<emphasis role="bold">CODE DE L\'URBANISME</emphasis>\n</title>\n<mediaobject>\n<imageobject>\n<imagedata fileref="image/uuid-6a55d7c8-5a31-15cb-0d58-6b3e4d907598.svg" xinfo:image="5258999" xinfo:image-description="" xinfo:image-filename="page_presentation_cdu_code_urbanisme.svg" xinfo:image-title="img-00_00_00_00_01_frontPageCdu.svg"/>\n</imageobject>\n</mediaobject>\n', 'attributes': {'role': 'titre', 'version': '5.0', 'xinfo:resource': 'UUID-8331f403-48d1-7433-e659-dfc7bd8dd4a5', 'fork_id': '5259006', 'xinfo:resource-id': '5259006', 'xinfo:resource-title': "Code de l'urbanisme", 'xinfo:resource-titlelabel': '', 'xinfo:resource-type': 'component fork', 'xinfo:version-major': '2', 'xinfo:version-minor': '2', 'xml:id': 'UUID-8331f403-48d1-7433-e659-dfc7bd8dd4a5', 'dir': 'ltr', 'xml:lang': 'fr', 'xinfo:origin': 'UUID-6b10868f-7bf0-92c6-22b7-22a4459fb90d', 'xinfo:origin-id': '5259000', 'xinfo:time-modified': '1681497647', 'xinfo:time-created': '1647655027', 'xinfo:linktype': 'ResourceLink'}}
        """      
        self.data = publication_xml  
        xml_soup = Soup(self.data, "xml")
        all_contents_list = []
        for section in xml_soup.find_all("section"):
            if v1:
                self.parsed_Topic_v1 += 1
                os.system('cls')
                print(f"Nombres de topics traité - v1: {self.parsed_Topic_v1}, v2: {self.parsed_Topic_v2}")
            
            #print(section)
            xml_attributes = section.attrs
            #print(xml_attributes)
            topic = {}
            attributes = {}
            if len(xml_attributes) != 0:
                if "xinfo:resource-title" in xml_attributes.keys():
                    for k, v in xml_attributes.items():
                        if k == 'xinfo:resource-id':
                            attributes.update({"fork_id": v})
                        attributes.update({k: v})
                    contents = section.contents
                    content_string = "".join(str(e) for e in contents)
                    #print(content_string)
                    topic.update({"content": content_string})
                    topic.update({"attributes": attributes})    
                    #print(topic)    
                    all_contents_list.append(topic)
                
        return all_contents_list
    
    def xml_string_v2(self, v2_paligo):
        content_list = []
        for topic in v2_paligo:
            self.parsed_Topic_v2 += 1
            content = topic[9]
            item_list = self.xml_string_v1(content, False)
            content_list.append(item_list[0])
            os.system('cls')
            print(f"Nombres de topics traité - v1: {self.parsed_Topic_v1}, v2: {self.parsed_Topic_v2}")
        
        return content_list    
            
    def revert_to_v1(self):
        json_reverting_list = read_data_from_json("list_articles_for_reverting.json")
        for i in json_reverting_list:
            v1_data = i["v1"]
            topic_id = v1_data["attributes"]["xinfo:origin-id"]
            if topic_id:
                t_content = """<section>""" +v1_data["content"] + """</section>"""
                content_soup = Soup(t_content, "xml")
                self.paligo_xml_info(content_soup)
                section = content_soup.section
                self.xmlns_info(section, v1_data["attributes"])
                
                for s in content_soup.section.contents:
                    #print(s)
                    if s.string != None:
                        if s.string.startswith("\nlink id"):
                            s.replace_with("\n")
                get_notes = content_soup.find_all("note")
                for note in get_notes:
                    note.extract()            
                get_subscripts = content_soup.find_all("subscript")
                for sub in get_subscripts:
                    if "merge-context" in sub.attrs:
                        del sub["merge-context"]        
                content_post = str(content_soup)
                #print(content_post)
                new_soup = Soup(str(content_post), "xml")
                #print(new_soup)
                new_content_post = str(new_soup)
                response = self.paligo_r.post_document_by_ids(self.paligo_r._document_url, int(topic_id), new_content_post)
                time.sleep(5)
                if response.status_code in [200, 201]:
                    print(f"Susccessfully reverted to v1: {topic_id}, stauts code: {response.status_code}")
                if response.status_code not in [200, 201]:
                    self.missed_revert_articles.append({"topic_id": topic_id, "status_code": response.status_code, "response": response.json(), "new_content_xml": new_content_post})
                    """response = self.paligo_r.post_document_by_ids(self.paligo_r._document_url, int(topic_id), new_content_post)
                    
                    if response.status_code not in [200, 201]:
                        time.sleep(30)
                        print(f"Error while posting check document id: {topic_id}")
        """
        save_data_to_json(self.missed_revert_articles, "missed_article_reverting.json")
    def has_class_text(self, tag: Soup):
        return tag.has_attr('text')
    def xmlns_info(self, section: Soup, v_data_attrs: dict):
        """Add XML classes to topic section

        Args:
            section (Soup): _description_
            v_data_attrs (dict): _description_
        """        
        section["xmlns"]= "http://docbook.org/ns/docbook"
        section["xmlns:mml"] = 'http://www.w3.org/1998/Math/MathML'
        section["xmlns:xinfo"] = "http://ns.expertinfo.se/cms/xmlns/1.0"
        section["xmlns:t"] = 'http://ns.expertinfo.se/translation/xmlns/1.0'
        section["xmlns:xlink"] = 'http://www.w3.org/1999/xlink'
        section["xinfo:version"] = "1"
        for k, v in v_data_attrs.items():
            if k in ["role"]:
                section[k] = v
    def paligo_xml_info(self, soup: Soup):
        tag = soup.new_tag("?xml-model")
        tag["href"] = "https://laval.paligoapp.com/schema/docbookxi-5.1-xinfo.rng"
        tag["type"] = "application/xml"
        tag["schematypens"] = "http://relaxng.org/ns/structure/1.0"
        soup.append(tag)
        #
        #print(tag)
        
    def paligo_xml_fct_change_a_class_name(self, content_soup: Soup, tag_targeted: str, old_class: str, new_class:str):
        """Paligo XML function to change a class name in all given tags in a section.

        Args:
            content_soup (Soup): the BeautifulSoup element of the topic content
            tag_targeted (str): the targeted tag
            old_class (str): the name of the existing class we want the name to be changed
            new_class (str): the NEW class name
        """        
        for tag in content_soup.section.find_all(tag_targeted):
            if old_class in tag.attrs:
                var = tag[old_class]
                del tag[old_class]
                tag[new_class] = var
    def paligo_xml_fct_change_a_tag_name(self, content_soup: Soup, tag_targeted: str, old_name: str, new_name:str):
        pass
    
    
    def revert_to_v2(self):
        
        """Revert content from Json file to the latest version
        """        
        json_reverting_list = read_data_from_json("list_articles_for_reverting.json")
        for i in json_reverting_list:
            
            v2_data = i["v2"]
            topic_id = v2_data["attributes"]["xinfo:resource-id"]
            check_match = [x for x in self.restart_list if x["topic_id"] == topic_id]
            if len(check_match) == 0:
                t_content = "<section>\n" +v2_data["content"] + "\n</section>"
                content_soup = Soup(t_content, "xml")
                self.paligo_xml_info(content_soup)
                section = content_soup.section
                self.xmlns_info(section, v2_data["attributes"])
                
                ### Rebuild Paligo variable-set element in topics
                for phrase in content_soup.section.find_all("phrase"):
                    x_var = phrase["variable"]
                    x_set = phrase["varset"]
                    del phrase["variable"]
                    del phrase["varset"]
                    
                    phrase["xinfo:variable"] = x_var
                    phrase["xinfo:varset"] = x_set
                    
                for text in content_soup.section.find_all(self.has_class_text):
                    del text["text"]
                content_post = str(content_soup)
                #print(content_post)
                new_soup = Soup(str(content_post), "xml")
                new_soup.section["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
                new_soup.section["xmlns:xi"] = "http://www.w3.org/2001/XInclude"
                # print(xi_include)
                new_soup.section["xmlns"] = "http://docbook.org/ns/docbook"
                new_soup.section["xmlns:xinfo"] = "http://ns.expertinfo.se/cms/xmlns/1.0"
                
                for include in new_soup.section.find_all("include"):
                    if include is not None:
                        include.name = "xi:include"
                for fallback in new_soup.section.find_all("fallback"):
                    if fallback is not None:
                        fallback.name = "xi:fallback"
                
                self.paligo_xml_fct_change_a_class_name(new_soup, "para", "translate", "xinfo:translate")
                self.paligo_xml_fct_change_a_class_name(new_soup, "imagedata", "image", "xinfo:image")
                self.paligo_xml_fct_change_a_class_name(new_soup, "phrase", "merge-context", "xinfo:merge-context")
                self.paligo_xml_fct_change_a_class_name(new_soup, "emphasis", "merge-context", "xinfo:merge-context")
                self.paligo_xml_fct_change_a_class_name(new_soup, "footnote", "merge-context", "xinfo:merge-context")
                self.paligo_xml_fct_change_a_class_name(new_soup, "superscript", "merge-context", "xinfo:merge-context")
                self.paligo_xml_fct_change_a_class_name(new_soup, "subscript", "merge-context", "xinfo:merge-context")
                self.paligo_xml_fct_change_a_class_name(new_soup, "para", "status", "xinfo:status")
                self.paligo_xml_fct_change_a_class_name(new_soup, "link", "href", "xlink:href")
                new_soup.section["xinfo:version"] = "2"
                #print(new_soup)
                new_content_post = str(new_soup)
                response = self.paligo_r.post_document_by_ids(self.paligo_r._document_url, int(topic_id), new_content_post)
                if response.status_code in [200, 201]:
                    print(f"Susccessfully reverted to v2: {topic_id}, stauts code: {response.status_code}")
                    self.restart_list.append({"topic_id": topic_id, "status_code": response.status_code})
                    save_data_to_json(self.restart_list, "paligo_rebuild_versionning\\temprestart_list_v2.json")
                while response.status_code not in [200, 201]:
                    response = self.paligo_r.post_document_by_ids(self.paligo_r._document_url, int(topic_id), new_content_post)
                    print(f"Error while posting check document id: {topic_id}")
                    time.sleep(30)
                time.sleep(3)
        save_data_to_json([], "paligo_rebuild_versionning\\temprestart_list_v2.json")
    def list_erors(self):
        list_error_topic_name = []
        errors = read_data_from_json("missed_article_reverting.json") 
        for e in errors:
            #print(e["new_content_xml"])
            soup_e  = Soup(str(e["new_content_xml"]), "xml")
            for title in soup_e.title.contents:
                if title not in ["", "\n"]:
                    list_error_topic_name.append(title.next)     
        save_data_to_json(list_error_topic_name, "paligo_rebuild_versionning\\correction_article_v1.json")
        print("Liste d'article sauvegardée")
    
    def revert_tobackup_v2(self):
        pass
        

    


if __name__ == "__main__":
    
    s_data = Find_topic_versions()
    app_up = True
    while app_up is True:
        user_input = input("""
                           
                           Option:
                           
                            - 1: Revert to v1
                            - 2: Revert to v2
                            - 3: List errors
                           
                           """)
        if user_input =="1":
            s_data.revert_to_v1()
        if user_input == "2":
            s_data.revert_to_v2()
            
        if user_input == "3":
            s_data.list_erors()
        elif user_input not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            app_up = False
            break