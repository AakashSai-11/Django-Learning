from rest_framework import generics, mixins, permissions, authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsStaffEditorPermission

'''class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_create(self,serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        print('Created Successfully')
        serializer.save()'''
        # -> This is used to create new data in the database
        
        
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated] # IsAuthenticated need permissions where as IsAuthenticatedOrReadOnly allows anyone to list the database but only authenticated ones can create the data
    permission_classes = [IsStaffEditorPermission]
    def perform_create(self,serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        print('Created Successfully')
        serializer.save()
    # This is the mix of create view and list view where the post will create data in the db and get request will list the db
product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
product_detail_view = ProductDetailAPIView.as_view()


class ProductListAPIView(generics.ListAPIView):
    '''
        For this we have to go for different endpoint to use it.
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
product_list_view = ProductListAPIView.as_view()



class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title   
            
    
product_update_view = ProductUpdateAPIView.as_view()


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


product_delete_view = ProductDeleteAPIView.as_view()

# All the above stuff is class based strong generic views, they actually can be done through functions as well in the below manner :-


@api_view(['GET','POST'])
def product_alt_view(request,pk=None ,*args, **kwargs):
    method = request.method # PUT -> Update and DELETE -> Destroy
    if method == 'GET':
        if pk is not None:
            # Detail view
            # queryset = Product.objects.all(pk = pk)
            # if not queryset.exist():
            #     raise Http404 -> This is one way
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # List view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    
    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            print('Created successfully')
            return Response(serializer.data)
    # -> This is equivalent to the above generic classes but this is the function style
    
# Mixing stuff :--

class ProductMixinView(mixins.CreateModelMixin ,mixins.ListModelMixin, mixins.RetrieveModelMixin ,generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def get(self, request, *args, **kwargs): # We can use POST also not only get and if we do that then also it will return the list
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, *kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self,serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        print('Created Successfully')
        serializer.save()
    

product_mixin_view = ProductMixinView.as_view()
            