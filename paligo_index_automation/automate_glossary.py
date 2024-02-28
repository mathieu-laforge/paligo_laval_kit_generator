from paligo_index_automation.extract_definitions import Extract_glossary
from paligo_index_automation.get_publication_content import Publication_content
from paligo_index_automation.text_tokenizer import Text_tokenizer
from bs4 import BeautifulSoup as Soup
from paligo_requests.paligo_requests import Paligo_request
from utils.sqlite_db_management import SqLite_DB_manager
import bs4
import re
import time
from utils.json_files import save_data_to_json

class Automate_glossary:
    tot_gloss_count = 0
    specific_gloss_count = {}
    
    def __init__(self, table_name: str, glossary_doc_id: int, ):
        self.table_name = table_name
        pub_c = Publication_content(self.table_name)
        self.publication_content = pub_c.get_sql_DB()
        x_gloss = Extract_glossary(glossary_doc_id)
        self.glossterm_list = x_gloss.glossterms()
        json_gloss_list = []
        """for i in self.glossterm_list:
            gloss_reference = i
            gloss_common_use = [""]
            json_gloss_list.append({"gloss_reference": gloss_reference, "gloss_common_use": gloss_common_use})
        save_data_to_json(json_gloss_list, "glossary_match_references.json")"""   
        self.paligo_r = Paligo_request("prod")
    
    def find_matching_words(self, specific_doc_id: int = None):
        for i in self.publication_content:
            if specific_doc_id is not None:
                if i[6] == str(specific_doc_id):
                    doc_id = i[6]
                    doc_name = i[7]
                    doc_content = i[9]
                    
                    content_soup = Soup(doc_content, "xml")
                    
                    self.construct_glossary(doc_id, content_soup, doc_name)
                else:
                    pass
            else:
                doc_id = i[6]
                doc_name = i[7]
                doc_content = i[9]
                content_soup = Soup(doc_content, "xml")
                self.construct_glossary(doc_id, content_soup, doc_name)
            ### To do: Essayer de reconstruire completement le para content... en faisant un append de tout le nouveau contenu
        save_data_to_json(self.specific_gloss_count, "specific_gloss_count.json")
    
    def construct_glossary(self, doc_id, content_soup: Soup, doc_name):             
        post = False
        
        for term in self.glossterm_list:
                
            #print(self.glossterm_list)
            for para in content_soup.find_all("para"):
                para_content: Soup = para.contents
                para_content_list = []
                for element in para_content:
                    if type(element) == bs4.element.NavigableString:
                        if element is not None:
                            lower_para_text = element.lower()
                            index = lower_para_text.find(term.lower())
                            if index != -1:
                                token = Text_tokenizer()
                                tokenize_text = token.tokenize(lower_para_text)
                                tokenize_term = token.tokenize(term.lower())
                                #print(tokenize_text)
                                confirm_token = [x for x in tokenize_text if x in tokenize_term]
                                #print(confirm_token)
                                if len(confirm_token) != 0:
                                    plurial_buffer = 0
                                    end_index = len(term) + index
                                    try:
                                        element[end_index]
                                        the_END_index = end_index
                                    except IndexError:
                                        print("invalid Index")
                                        the_END_index = end_index-1
                                    finally: 
                                        if element[the_END_index] == "s":
                                            plurial_buffer = +1
                                        if element[the_END_index] in ["s", " ", ";", ",", "."]:
                                            #print(element[end_index])
                                            part1 = element[:index]
                                            gloss = element[index: the_END_index + plurial_buffer]
                                            if the_END_index != end_index-1:
                                                part2 = element[the_END_index + plurial_buffer:]
                                            else:
                                                part2 = ""
                                            new_text = "<para>"+part1+f"""<glossterm baseform="{term}">{gloss}</glossterm>"""+part2+"</para>"
                                            soup_element = Soup(new_text, "xml")
                                            new_elements = soup_element.para.contents
                                            self.tot_gloss_count +=1
                                            for e in new_elements:
                                                para_content_list.append(e)
                                            post = True
                                        else:
                                            para_content_list.append(element)
                                else:
                                    para_content_list.append(element) 
                            if index == -1:
                                para_content_list.append(element)               
                    else:
                        para_content_list.append(element)
                
                para.clear()
                
                for e in para_content_list:
                    para.append(e)
                    
            
            content_soup = Soup(str(content_soup), "xml")                    
        if post is True:
            response = self.paligo_r.post_document_by_ids(self.paligo_r._document_url, doc_id, str(content_soup))                      
            status = response.status_code
            updated_data = response.json()
            print(f"Document posted - status code: {status} - doc name: {doc_name}")
            
            
            if status in [200, 201]:
                update_id = updated_data["id"]
                update_content = updated_data["content"]
                paligo_db = SqLite_DB_manager("db/paligo.db", self.table_name)
                paligo_db.update_data("doc_id = ?, doc_content = ?", "doc_id", (update_id, update_content, update_id))
                print(f"Total glossentry added: {self.tot_gloss_count}")
                print("system sleep for 10 seconds")
                time.sleep(10)
            else:
                print(f"Failed to update Paligo - status code: {status} - doc name: {doc_name} - {updated_data}")

if __name__ == '__main__':
    atm = Automate_glossary("cdu_publication", 10381520)
    atm.find_matching_words()
    