import requests
import json

book1 = {
  'id': 4,
  'title': '1984',
  'author': 'George Orwell',
  'rating': 4.18,
  'pages': 387
}

book2 = {
  'id': 5,
  'title': 'Lord of the Flies',
  'author': 'William Golding',
  'rating': 3.68,
  'pages': 112
}

response = requests.post('https://htn-api.jayantsh.repl.co/', json = book1)

print(json.dumps(response.json(), indent=2))