from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Collection
from .serializers import CollectionSerializers

class CollectionView(APIView):
    def get(self, request):
        queryset = Collection.objects.order_by('pk').all()
        serializer = CollectionSerializers(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CollectionSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CollectionDetailsView(APIView):
    def get(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializers(queryset)
        return Response(serializer.data)
    
    def put(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializers(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)