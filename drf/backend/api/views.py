import json
from django.http import JsonResponse
from django.forms.models import model_to_dict # The way to convert model instances to dictionaries
from products.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer

def basics(request, *args, **kwargs):
    body = request.body # We get byte string of json data
    data =  {}
    try:
        data = json.loads(body) # Converts byte of json data to python dictionary
    except:
        pass
    data['headers'] = dict(request.headers)
    data["params"] = dict(request.GET)
    data['content_type'] = request.content_type
    print(request.GET) # Give the query parameters of the request
    return JsonResponse(data) #Dictionary to json
    # Remember that while returning you have to return something like Response(), JsonResponse(), HttpResponse()
    # If not django will not accept it



def first(request, *args, **kwargs):
    model_data = Product.objects.all().first()
    data = {}
    print(model_data)  # <QuerySet [<Product: Product object (1)>, <Product: Product object (2)>]>
    if model_data:
        data = model_to_dict(model_data)
            
    return JsonResponse(data)

# The above ones are normal apis, we can easily convert them to rest apis by doing this :-


@api_view(['GET', 'POST']) #Django REST framework api view from now on
def api_home(request, *args, **kwargs):
    instance = Product.objects.all().first()
    data = {}
    if request.method == 'GET':
        if instance:
        #     data = model_to_dict(model_data)
            data = ProductSerializer(instance).data
        return Response(data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # instance = serializer.save() # The saved Product is returned here, that is a new instance in the database or a new basically
            # print(instance)
            
            return Response(serializer.data)
        

