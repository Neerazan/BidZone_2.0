from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Collection
from .serializers import CollectionSerializers

class CollectionView(APIView):
    def get(self, request):
        queryset = Collection.objects.all()
        serializer = CollectionSerializers(queryset, many=True)
        return Response(serializer.data)