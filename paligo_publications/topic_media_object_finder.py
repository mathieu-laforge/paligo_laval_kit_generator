from bs4 import BeautifulSoup as Soup

class Topic_media_objects_finder:
    def __init__(self):
        self.find = "mediaobject"
    
    def media_objects_finder(self, content: str):
        content_soup = Soup(content, "xml")
        find_all_media = content_soup.find_all(self.find)
        return find_all_media