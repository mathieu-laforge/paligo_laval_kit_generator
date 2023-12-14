

import requests
import os
import base64
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
import config as cfg
from utils.app_settings import app_settings

__PALIGO_CLIENT__PROD__ = cfg.paligoConnect["auth"]


class Thread_Paligo_Request:
    """Send requests with threads
    
    Arguments:
    -----------
    url (str):
        The url to send requests
    environment (str):
        'prod' or 'dev' to send requests
    max_threads (int):
        the maximum number of threads to send requests
    param_list (list):
        The list of changing parameters for each requests as: `[{"name": str, "id": int, "content": str}, ...]`
    timeout (int):
        The timeout for requests to respond
    data
    """
    def __init__(self,url: str, environment: str, max_threads: int,  param_list: list, timeout: None | int):
        if environment == "prod":
            self.apiKey = str(base64.b64encode(__PALIGO_CLIENT__PROD__.encode('ascii')))
        elif environment == "dev":
            #self.apiKey = str(base64.b64encode(__PALIGO_CLIENT__DEV__.encode('ascii')))
            pass
        else:
            raise ValueError ("Invalid environment, must be 'dev' or 'prod'")
        self.get_header = {
            'Accept': 'application/json',
            'Authorization': "basic" + self.apiKey,
        }
        self.post_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': "basic" + self.apiKey,
        }
        self.max_threads = max_threads
        self.url = url
        self.param_list = param_list
        self.timeout = timeout
    
    def put_requests(self, post_list):  
        
        topic_id = post_list["id"]
        topic_content = post_list["content"]
            
        input_body = {
            "content": str(topic_content),
            "checkout": "false",
        }
        time.sleep(3)
        print("Put Request: ", post_list["name"])
        return requests.put(self.url + str(topic_id), headers=self.post_header, data=json.dumps(input_body))

    def thread_put(self):
        with ThreadPoolExecutor(max_workers=self.max_threads) as pool:
            response_list = list(pool.map(self.put_requests, self.param_list))
        all_responses = []

        for response in response_list:
            print(response.status_code)
            data = response.json()
            all_responses.append(data)

        return all_responses
    
    def post_requests(self, post_list):  
        #print(post_list)
        topic_parent = post_list["parent"]
        topic_name = post_list["name"]
        topic_content = post_list["content"]
        topic_subtype = post_list["subtype"]
        input_body = {
            "parent": int(topic_parent),
            "name": str(topic_name),
            "content": str(topic_content),
            "subtype": str(topic_subtype)
        }
        time.sleep(0.5)
        print("Post Request: ", post_list["name"])
        return requests.post(self.url, headers=self.post_header, data=json.dumps(input_body))

    def thread_post(self):
        with ThreadPoolExecutor(max_workers=self.max_threads) as pool:
            response_list = list(pool.map(self.post_requests, self.param_list))
        all_responses = []

        for response in response_list:
            print(response.status_code)
            data = response.json()
            all_responses.append(data)

        return all_responses

    def get_requests(self):  
        time.sleep(0.5)
        return requests.get(self.url, headers=self.get_header)

    def thread_get(self):
        with ThreadPoolExecutor(max_workers=self.max_threads) as pool:
            response_list = list(pool.map(self.get_requests, self.param_list))
        all_responses = []

        for response in response_list:
            print(response.status_code)
            data = response.json()
            all_responses.append(data)

        return all_responses

class Paligo_request:
    """
    Get a document from Paligo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    arguments:
        "prod" or "dev"
    
    """

    def __init__(self, environment: str):
        if environment == "prod":
            self.apiKey = str(base64.b64encode(__PALIGO_CLIENT__PROD__.encode('ascii')))
        else:
            if environment == "dev":
                pass
                #self.apiKey = str(base64.b64encode(__PALIGO_CLIENT__DEV__.encode('ascii')))
        
        self.get_header = {
            'Accept': 'application/json',
            'Authorization': "basic" + self.apiKey,
        }
        self.post_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': "basic" + self.apiKey,
        }
        self.outputs_headers = {
            'Accept':'application/zip',
            'Authorization': "basic" + self.apiKey,
        }
        self._folder_url = app_settings("prod_paligo_request", "request", "folder")[0][1]
        self._document_url = app_settings("prod_paligo_request", "request", "document")[0][1]
        self._forks_url = app_settings("prod_paligo_request", "request", "forks")[0][1]
        self._taxonomies_url = app_settings("prod_paligo_request", "request", "taxonomies")[0][1]
        self._outputs_url = app_settings("prod_paligo_request", "request", "outputs")[0][1]
        self._production_url = app_settings("prod_paligo_request", "request", "production")[0][1]
        self._publish_url = app_settings("prod_paligo_request", "request", "publish")[0][1]

    def get_document_by_ids(self, _url: str, _id: int, _full_response: bool | None):
        """
        ### GET method for Paligo documents by IDs
            1. url = string url of your api
            2. id = int ID of your document in Paligo
        """
        # print("Téléchargement des dernières tables à jour de Paligo...")
        try:
            response = requests.get(
                _url+str(_id), headers=self.get_header)
        except Exception as e:
            print(
                "Request Error: " + e)
        finally:
            topicData = response.json()
            if _full_response is None or _full_response is False:
                topicContent = topicData["content"]
                return topicContent
            else:
                return topicData

    def get_any_document(self, _url: str, _id: int):
        """
        ### GET method for Paligo documents by IDs
            1. url = string url of your api
            2. id = int ID of your document in Paligo
        """
        # print("Téléchargement des dernières tables à jour de Paligo...")
        try:
            response = requests.get(
                _url+str(_id), headers=self.get_header)

        except Exception as e:
            print(
                "Request Error: " + e)
        finally:

            return response.json()

    def post_publications_forks(self, _url: str, document_id: int, _parent_fork_id : int):
        r""":POST method for Paligo documents by IDs

        :_url:    string url of your api

        :document_id:    int ID of your document in Paligo

        :_parent_fork_id:    string of xml content of the topic
        """
        body_params = {
            "parent": _parent_fork_id,
            "document": document_id,
            }
        response = requests.post(_url, headers=self.post_header, data=json.dumps(body_params), timeout=600)
        return response.status_code
    
    def post_publications_forks_with_order(self, _url: str, document_id: int, _parent_fork_id : int, position: str):
        r""":POST method for Paligo documents by IDs

        :_url:    string url of your api

        :document_id:    int ID of your document in Paligo
        
        :position:    string of the position of the element

        :_parent_fork_id:    string of xml content of the topic
        """
        body_params = {
            "parent": _parent_fork_id,
            "document": document_id,
            "position": position
            }
        response = requests.post(_url, headers=self.post_header, data=json.dumps(body_params), timeout=600)
        return response.status_code
    
    def delete_paligo_forks(self, _url: str, fork_id: int):
        """_summary_

        Args:
            _url (str): Url of forks requests
            fork_id (int): Fork id of the fork to delete from publication.

        Returns:
            int: status code of the request `204` is success
        """        
        response = requests.delete(_url+str(fork_id), headers=self.get_header, timeout=600)
        return response.status_code
    
    def post_document_by_ids(self, _url, _id, _content):
        r""":POST method for Paligo documents by IDs

        :_url:    string url of your api

        :_id:    int ID of your document in Paligo

        :_content:    string of xml content of the topic
        """
        try:
            body_params = {
                "content": _content,
                "checkout": "false",
            }
            response = requests.put(
                _url+str(_id), headers=self.post_header, data=json.dumps(body_params))
            topicData = response.json()
            #print(topicData, response.status_code)
            return response

        except json.JSONDecodeError as jsonE:
            print("Il y a une erreur de décodage JSON. Veuillez vérifier manuellement que le topic est à jour. https://laval.paligoapp.com/login")
            print(response.status_code)
            print(jsonE)
        except requests.RequestException as requestsE:
            print("Erreur dans la requête")
            print(requestsE)
            print(response.status_code)

    def get_folder_by_ids(self, _url: str, _id: int):
        """
        ### GET method for Paligo documents by IDs
            1. url = string url of your api
            2. id = int ID of your document in Paligo
        """
        # print("Téléchargement des dernières tables à jour de Paligo...")
        try:
            response = requests.get(
                _url+str(_id), headers=self.get_header)
        except Exception as e:
            print(
                "Request Error: " + e)
        finally:
            folderData = response.json()

            return folderData

    def get_list_of_documents_by_params(self, _url: str, _parent: int):
        """
        ### GET method for Paligo documents by IDs
            1. url = string url of your api
            2. parent = int ID of your parent document

            Returns a list of documents under the parent ID
        """
        time.sleep(1)
        params = {
            "parent": str(_parent)
        }
        try:
            response = requests.get(
                _url, headers=self.get_header, params=params)
        except Exception as e:
            print(
                "Request Error: " + e)
        finally:
            list_documents = response.json()

        return list_documents
      
    def paligo_list_generator(self, _url: str, _parent: int, _timeout=300, _stream=False):
        
        session = requests.Session()

        first_page = session.get(_url, headers=self.get_header, params={"parent": str(_parent)}, timeout=_timeout, stream=_stream).json()
        yield first_page
        num_pages = first_page['total_pages']

        for page in range(2, num_pages + 1):
            print("Sending requests for page: " + str(page) + " of " + str(num_pages) + " in folder: " + str(_parent))
            next_page = session.get(_url, headers=self.get_header, params={"page": page, "parent": str(_parent)}).json()
            yield next_page
            
    def paligo_create_document(self, post_url: str, topic_parent: str, topic_name: str, topic_content: str, topic_subtype: str):
        input_body = {
            "parent": int(topic_parent),
            "name": str(topic_name),
            "content": str(topic_content),
            "subtype": str(topic_subtype)
        }
        headers = self.post_header
        
        try:
            response = requests.post(
                post_url, headers=headers, data=json.dumps(input_body))
        except Exception as e:
            print(
                "Request Error: " + e)
        finally:
            status = response.status_code
            r_json = response.json()
        
        return response
        
    def list_productions(self, _url: str):
        try:
            response = requests.get(
                _url, headers=self.get_header)
        except Exception as e:
            print(
                "Request Error: " + e)
        finally:
            status = response.status_code
            r_json = response.json()
            #print(status)
        
        return r_json
    
    def list_single_production(self, _url: str, production_id:str):
        try:
            response = requests.get(
                _url + production_id, headers=self.get_header)
        except Exception as e:
            print(
                "Request Error: " + e)
        finally:
            status = response.status_code
            r_json = response.json()
            #print(status)
        
        return r_json
    
    def list_publish_settings(self, _url: str):
        session = requests.Session()

        first_page = session.get(_url, headers=self.get_header).json()
        yield first_page
        num_pages = first_page['total_pages']

        for page in range(2, num_pages + 1):
            print("Sending requests for page: " + str(page) + " of " + str(num_pages))
            next_page = session.get(_url, headers=self.get_header, params={"page": page}).json()
            yield next_page
    
    def start_publishing(self, _url: str, _prod_name: str):
        input_body = {
            "publishsetting": _prod_name
        }
        headers = self.post_header
        
        try:
            response = requests.post(
                _url, headers=headers, data=json.dumps(input_body))
        except Exception as e:
            print(
                "Request Error: " + e)
        finally:
            status = response.status_code
            r_json = response.json()
            #print(status)
        
        return r_json
    
    def outputs_from_url(self, _url: str):
        headers = self.outputs_headers
        try:
            response = requests.get(_url, headers=headers)
        except Exception as e:
            print("Request Error: " + e)
        finally:
            r_stream = response.content
            return r_stream