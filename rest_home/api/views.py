#from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
'''
class RestHomeListView(ListAPIView):
	queryset = RestHome.objects.all()
	serializer_class = RestHomeSerializer

class RestHomeRetrieveView(RetrieveAPIView):
	queryset = RestHome.objects.all()
	serializer_class = RestHomeSerializer

class RestHomeCreateView(CreateAPIView):
	queryset = RestHome.objects.all()
	serializer_class = RestHomeSerializer

class RestHomeDeleteView(DestroyAPIView):
	queryset = RestHome.objects.all()
	serializer_class = RestHomeSerializer

class RestHomeUpdateView(UpdateAPIView):
	queryset = RestHome.objects.all()
	serializer_class = RestHomeSerializer'''

from rest_framework import viewsets
from rest_home.models import RestHome
from .serializers import RestHomeSerializer

class RestViewSet(viewsets.ModelViewSet):
    serializer_class = RestHomeSerializer
    queryset = RestHome.objects.all()

