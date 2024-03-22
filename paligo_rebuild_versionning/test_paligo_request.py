from paligo_requests.paligo_requests import Paligo_request

paligo_r = Paligo_request("prod")

response = paligo_r.get_document_by_ids(paligo_r._document_url, 1490893, True)

print (response)