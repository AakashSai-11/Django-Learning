import requests

# endpoint = 'https://httpbin.org/'
endpoint = 'http://127.0.0.1:8000/api/'

get_response = requests.post(endpoint , json={"title":"Yo boys"})
# The part involving json parameter is considered as the request body

print(get_response.json())