from extract_definitions import Extract_glossary
from get_publication_content import Publication_content
from text_tokenizer import Text_tokenizer
from bs4 import BeautifulSoup as Soup
from paligo_requests.paligo_requests import Paligo_request
import bs4
import re

class Automate_glossary:
    def __init__(self, table_name: str, glossary_doc_id: str, ):
        pub_c = Publication_content(table_name)
        self.publication_content = pub_c.get_sql_DB()
        x_gloss = Extract_glossary(glossary_doc_id)
        self.glossterm_list = x_gloss.glossterms()
        self.paligo_r = Paligo_request("prod")
    
    def find_matching_words(self):
        for i in self.publication_content:
            doc_id = i[6]
            doc_content = i[9]
            content_soup = Soup(doc_content, "xml")
            post = False
            for para in content_soup.find_all("para"):
                para_content: Soup = para.contents
                for element in para_content:
                    print(element.index)
                    print(element)
                    print(type(element))
                    if type(element) == bs4.element.NavigableString:
                        
                        for term in self.glossterm_list:
                            if element is not None:
                                lower_para_text = element.lower()
                                index = lower_para_text.find(term.lower())
                                if index != -1:
                                    print(index)
                                    print(element)
                                    print(term)
                                    end_index = len(term) + index
                                    part1 = element[:index]
                                    gloss = element[index: end_index]
                                    part2 = element[end_index:]
                                    print(part1, gloss, part2)
                                    new_text = "<para>"+part1+f"""<glossterm baseform="{term}">{gloss}</glossterm>"""+part2+"</para>"
                                    soup_element = Soup(new_text, "xml")
                                    new_elements = soup_element.para.contents
                                    element.replace_with(new_elements)
                                    post = True
                                    
            if post is True:
                response = self.paligo_r.post_document_by_ids(self.paligo_r._document_url, doc_id, str(content_soup))                      
                print(response)                
      
                         
    def new_para(self, content_soup:Soup):
        tag_para = content_soup.new_tag("para")
        tag_gloss_term = content_soup.new_tag
if __name__ == '__main__':
    atm = Automate_glossary("cdu_publication", 10381520)
    atm.find_matching_words()