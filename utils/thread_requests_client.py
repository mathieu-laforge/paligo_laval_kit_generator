import requests
from requests import RequestException
from concurrent.futures import ThreadPoolExecutor
import time

class Threads_requests_client():
    def __init__(self, url, request_subject=None, payload=None, sleep=None, max_workers=None, authentication=None):
        self.list_range = len(url)
        if payload is None: 
            payload = [None] * self.list_range
        
        
        self.url = url
        self.request_subject = request_subject
        self.payload = payload
        self.sleep = sleep
        self.max_workers = max_workers
        self.authentication = authentication
        self.thread_requests_pool()
        
    def requests_constructor(self, _url, _request_subject, _payload):
        
        headers = {}
        if self.authentication is not None:
            headers['Authorization'] = self.authentication
        if self.payload is not None:
            data = _payload
        else:
            data = ""
        if _request_subject is not None:
            request_url = _url+str(_request_subject)
        else:
            request_url = _url
        time.sleep(self.sleep)
        print("Sending request for {}".format(_request_subject))
        return requests.get(request_url, headers=headers, data=data)
        

    def thread_requests_pool(self):
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                response_list = list(pool.map(self.requests_constructor, self.url, self.request_subject, self.payload))
            all_responses = []
            
            for response in response_list:
                print(response.status_code)
                if response.status_code == 200:
                    data = response.json()
                    all_responses.append(data)
                if response.status_code == 500:
                    pass
            return all_responses
        except RequestException as e:
            print(e)
        except Exception as e:
            print(e)