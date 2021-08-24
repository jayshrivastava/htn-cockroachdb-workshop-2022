import requests

response = requests.delete('https://htn-api.jayantsh.repl.co/1')

print(response.json())