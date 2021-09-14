import requests
import json

# response = requests.get('http://htn-api.jayantsh.repl.co/')
# print(json.dumps(response.json(), indent=2))
response = requests.get('http://htn-api.jayantsh.repl.co/0')
print(json.dumps(response.json(), indent=2))
# response = requests.get('http://htn-api.jayantsh.repl.co/search?max_pages=360&min_rating=4')
# print(json.dumps(response.json(), indent=2))
