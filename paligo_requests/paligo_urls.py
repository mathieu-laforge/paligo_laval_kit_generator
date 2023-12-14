from utils.app_settings import app_settings

class paligo_requests_url:
    def __init__(self):
        self.folder_url = app_settings("prod_paligo_request", "request", "folder")[0][1]
        self.document_url = app_settings("prod_paligo_request", "request", "document")[0][1]
        self.forks_url = app_settings("prod_paligo_request", "request", "forks")[0][1]
        self.taxonomies_url = app_settings("prod_paligo_request", "request", "taxonomies")[0][1]
        self.outputs_url = app_settings("prod_paligo_request", "request", "outputs")[0][1]
        self.production_url = app_settings("prod_paligo_request", "request", "production")[0][1]
        self.publish_url = app_settings("prod_paligo_request", "request", "publish")[0][1]
    
    def prod_urls(self):
        return {
            "folder": self.folder_url, 
            "document": self.document_url, 
            "forks": self.forks_url,
            "taxonomies": self.taxonomies_url,
            "outputs": self.outputs_url,
            "production": self.production_url,
            "publish": self.publish_url
            }