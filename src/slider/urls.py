from rest_framework_nested import routers

from .views import SliderViewSet

router = routers.DefaultRouter()
router.register('items', SliderViewSet)

urlpatterns = router.urls