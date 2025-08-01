import requests

endpoint = 'http://localhost:8000/api/products/5/update/'

stuff = {
    "title":"Mahesh Babu",
    "price":30
}

get_response = requests.patch(endpoint, json=stuff)
print(get_response.json())