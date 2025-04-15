from paligo_requests.paligo_requests import Paligo_request

def test():
    request = Paligo_request("prod")
    
    multipage_forks = []
    response = request.paligo_list_generator(request._forks_url, 42898481)
    
    for r in response:
        if "total_pages" in r:
            forks = r["forks"]
            for f in forks:
                multipage_forks.append(f)
        multipage_forks = {"forks": multipage_forks}    
        print(multipage_forks)
if __name__ == "__main__":
    test()