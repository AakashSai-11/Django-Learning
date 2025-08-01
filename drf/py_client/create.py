import requests

endpoint = 'http://localhost:8000/api/products/'

stuff = {
    "title":"Babu",
    "content":"Hello Babu",
    "price":25
}

get_response = requests.post(endpoint, json=stuff)
print(get_response.json())