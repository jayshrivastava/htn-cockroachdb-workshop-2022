import requests
import json

response = requests.delete('https://htn-cockroachdb-workshop-2022.jayantsh.repl.co/1004098')

print(json.dumps(response.json(), indent=2))