from utils.sqlite_db_management import SqLite_DB_manager
from paligo_requests.paligo_requests import Paligo_request
from bs4 import BeautifulSoup as Soup
import config as cfg

def tag_list_for_kits():
    paligo_r = Paligo_request("prod")
    taxonomies_id = cfg.taxonomies_id
    fiches_tag_parents = cfg.fiches_tags
    
    response = paligo_r.paligo_list_generator(paligo_r._taxonomies_url, taxonomies_id)
    tag_list_for_fiches = []
    for r_list in response:
        for r in r_list["taxonomies"]:
            if r["title"] in fiches_tag_parents:
                tags = paligo_r.paligo_list_generator(paligo_r._taxonomies_url, r["id"])
                for t_list in tags:
                    for t in t_list["taxonomies"]:
                        tag_list_for_fiches.append(t)
    
    #print(tag_list_for_fiches)
        
    return tag_list_for_fiches

def tag_replacements_names():
    paligo_r = Paligo_request("prod")
    lexique_id = cfg.lexiques_id
    
    response = paligo_r.get_document_by_ids(paligo_r._document_url, lexique_id, True)
    table_data = parse_paligo_tables(response)
    return table_data

def parse_paligo_tables(response):
    if response["content"] is not None:
        content_soup = Soup(response["content"], 'xml')
        tables = content_soup.find_all("informaltable")
        all_rows = []
        for t in tables:
            table_headers = t.find_all("th")
            headers = []
            for th in table_headers:
                th:Soup
                if th.para.string is None:
                    headers.append(th.para.emphasis.string)
                else:
                    headers.append(th.para.string)
                
            table_rows = t.tbody.find_all("tr")
            
            
            for row in table_rows:
                row:Soup
                table_cells = row.find_all("td")
                row_data = {}
                for index, td in enumerate(table_cells):
                    td:Soup
                    cell_data = td.para.string
                    row_data.update({str(headers[index]): cell_data})
                all_rows.append(row_data)
        return all_rows

def get_paligo_content_by_tag(tag: str):
    """find all articles matching the given tag

    Args:
        tag (str): tag_name to look for...

    Returns:
        matching_articles (list): A list of articles full data from DB
    """    
    
    db = SqLite_DB_manager("db/paligo.db", "")
    list_tables = db.list_all_tables()
    #print(list_tables)
    publications_list = []
    for i in list_tables:
        if not str(i[0]).endswith(("tag_by_id", "tag_list", "stats", "warnings")):
            publications_list.append(i[0])

    matching_articles = []
    
    for table in publications_list:
        all_rules = SqLite_DB_manager("db/paligo.db", table)
        data_set = all_rules.fetch_all_data(f"WHERE doc_taxonomies LIKE '%{tag}%'")
        matching_articles.extend(data_set)    
    articles_list = []
    for article in matching_articles:
        articles_list.append(article[7])
    print(articles_list)
    return matching_articles

    

if __name__ == "__main__":
    #get_paligo_content_by_tag("batiment")
    tag_replacements_names()