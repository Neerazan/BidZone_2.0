from rest_framework.views import APIView
from django.db.models.aggregates import Count
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .models import Collection, Product, Review, Customer
from .serializers import CollectionSerializers, ProductSerializers, ReviewSerializers, CustomerSerializers


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializers



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()  
    serializer_class = ProductSerializers


class ReviewViewSet(ModelViewSet):
    
    def get_queryset(self):
        return Review.objects.filter(seller_id=self.kwargs['customer_pk'])
    
    serializer_class = ReviewSerializers

    def get_serializer_context(self):
        return {'seller_id': self.kwargs['customer_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializers

# class ProductList(APIView):
    #TODO: Optimize Query Problem

    # def get(self, request):
    #     queryset = Product.objects.all()
    #     serializer = ProductSerializers(queryset, many=True)
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = ProductSerializers(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetails(APIView):
    # def get(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializers(product)
    #     return Response(serializer.data)
    
    # def put(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializers(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    # def delete(self, request, pk):
    #     product = Product.objects.get(pk=pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)