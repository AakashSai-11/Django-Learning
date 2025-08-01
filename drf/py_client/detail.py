import requests
product_id = input('Enter the id')
product_id = int(product_id)

endpoint = f'http://localhost:8000/api/products/{product_id}'

stuff = {
    "title":"Ray",
    "content":"Hello World",
    "price":25
}

get_response = requests.get(endpoint)
print(get_response.json())