from rest_framework.generics import ListAPIView

from rest_home.models import RestHome
from .serializers import RestHomeSerializer

class RestHomeRetrieveView(ListAPIView):
	queryset = RestHome.objects.all()
	serializer_class = RestHomeSerializer

