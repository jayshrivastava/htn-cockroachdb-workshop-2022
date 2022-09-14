import requests
import json

response = requests.delete('https://htn-cockroachdb-workshop.jayantsh.repl.co/1004098')

print(json.dumps(response.json(), indent=2))