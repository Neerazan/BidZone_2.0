from rest_framework import serializers

from .models import Slider


class SliderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'title', 'image', 'url', 'status']
