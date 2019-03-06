from django.urls import path

from .views import RestHomeRetrieveView

urlpatterns = [
	path('', RestHomeRetrieveView.as_view()),
]