from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Slider
from .serializers import SliderSerializers


class SliderView(APIView):
    def get(self, request):
        queryset = Slider.objects.all()
        serializer = SliderSerializers(queryset, many=True)
        return Response(serializer.data)