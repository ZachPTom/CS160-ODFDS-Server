from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('driver', views.DriverViewSet)
router.register('restaurant', views.RestaurantViewSet)

urlpatterns = router.urls
