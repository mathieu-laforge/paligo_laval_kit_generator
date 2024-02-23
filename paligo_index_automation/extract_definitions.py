from paligo_requests.paligo_requests import Paligo_request
from bs4 import BeautifulSoup as Soup

class Extract_glossary:
    def __init__(self, definitions_topic_ID):
        """Extracts all glossentry in given topic 

        Args:
            definitions_topic_ID (int): the ID of a glossary in Paligo
            
        """        
        self.paligo_r = Paligo_request("prod")
        self.doc_url = self.paligo_r._document_url
        self.definitions_topic_ID = definitions_topic_ID
        
    def glossterms(self):
        """Make a list of all glossterm

        Returns:
            (list): List of string of every glossterm in the glossary
        """        
        glossterm_list = []
        glossary = self.get_glossary()
        gloss_content = glossary["content"]
        content_soup = Soup(gloss_content, "xml")
        
        for i in content_soup.find_all("glossterm"):
            glossterm_list.append(i.string)
        return glossterm_list
    
    def get_glossary(self):
        response = self.paligo_r.get_any_document(self.doc_url, self.definitions_topic_ID)
        return response
        #10381520
        
    
        
if __name__ == "__main__":
    x = Extract_glossary(10381520)
    x.glossterms()