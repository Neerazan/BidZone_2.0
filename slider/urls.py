from django.urls import path, include
from .views import SliderView

urlpatterns = [
    path('content/', SliderView.as_view())
]
