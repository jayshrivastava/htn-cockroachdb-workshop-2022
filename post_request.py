import requests
import json

new_airbnb = {
  'title': 'Nice Studio by the Water',
  'name': 'Jay',
  'neighbourhood': 'Brooklyn',
  'neighbourhood_group': 'Williamsburg',
  'verified': True, 
  'year': 2002
}


response = requests.post('https://htn-cockroachdb-workshop-2022.jayantsh.repl.co', json = new_airbnb)

print(json.dumps(response.json(), indent=2))