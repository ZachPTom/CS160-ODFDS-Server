'''from django.urls import path

from .views import RestHomeListView, RestHomeRetrieveView, RestHomeCreateView, RestHomeDeleteView, RestHomeUpdateView

urlpatterns = [
	path('', RestHomeListView.as_view()),
	path('create/', RestHomeCreateView.as_view()),
	path('<pk>', RestHomeRetrieveView.as_view()),
	path('<pk>/delete/', RestHomeDeleteView.as_view()),
	path('<pk>/update/', RestHomeUpdateView.as_view()),
]'''

from rest_home.api.views import RestViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', RestViewSet, basename='rest')
urlpatterns = router.urls