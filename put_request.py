import requests
import json

new_data = {
  'author': 'Robert L. Stevenson'
}

response = requests.put('http://htn-api.jayantsh.repl.co/2', json = new_data)

print(json.dumps(response.json(), indent=2))
