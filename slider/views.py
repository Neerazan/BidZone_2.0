from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser

from .models import Slider
from .serializers import SliderSerializers


class SliderViewSet(ModelViewSet):

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at']
    permission_classes = [IsAdminUser]

    queryset = Slider.objects.all()
    serializer_class = SliderSerializers