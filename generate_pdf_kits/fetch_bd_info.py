from utils.sqlite_db_management import SqLite_DB_manager

def get_all_kits_for_info():
    kits_list_by_tag = []
    
    for i in ["t5_general","t5_utilisation_cours", "t5_utilisation_toits", "tab_t5_utilisation_cours", "tab_t5_utilisation_toits"]:
        all_rules = SqLite_DB_manager("db/paligoAllRules.db", "validations_rules")
        data_set = all_rules.fetch_all_data(f"WHERE parentTagId LIKE '{i}'")
        kits_list_by_tag.extend(data_set)    
    
    return kits_list_by_tag

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
    get_paligo_content_by_tag("batiment")