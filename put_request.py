import requests
import json

new_data = {
  'title': 'Small Cozy 1 Bedroom Apartment In Midtown West'
}

response = requests.put('https://htn-cockroachdb-workshop-2022.jayantsh.repl.co/1004098', json = new_data)

print(json.dumps(response.json(), indent=2))
