import requests
import json

new_data = {
  'author': 'Robert L. Stevenson'
}

response = requests.put('https://htn-api.jayantsh.repl.co/3', json = new_data)

print(json.dumps(response.json(), indent=2))