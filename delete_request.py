import requests
import json

response = requests.delete('https://htn-api.jayantsh.repl.co/1')

print(json.dumps(response.json(), indent=2))