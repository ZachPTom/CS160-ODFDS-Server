from django.http import HttpResponse
from api.models import Driver, Restaurant
from api.serializers import DriverSerializer, RestaurantSerializer
from rest_framework import viewsets
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# Create your views here.
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    parser_classes = (JSONParser,)

    @detail_route(methods=['post'], url_path='login')
    def login(self, request, pk=None):
        email = request.data['email']
        test = RestaurantViewSet.queryset.filter(email=email)
        return Response(str(test))


