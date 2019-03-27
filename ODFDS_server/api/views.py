from django.http import HttpResponse
from api.models import Driver, Restaurant, Order
from api.serializers import DriverSerializer, RestaurantSerializer
from rest_framework import viewsets
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from functools import wraps
from math import sqrt


def session_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session = args[1].session.get('id', None)
        if not session:
            return HttpResponse('Not logged in', status=401)
        return f(*args, **kwargs)
    return wrapper


def find_driver(rest_id):
    rest_lat = Restaurant.objects.get(id=rest_id).rest_lat
    rest_long = Restaurant.objects.get(id=rest_id).rest_long
    distance = 2**10
    print(list(Driver.objects.filter(occupied=False)))
    for driver in Driver.objects.filter(occupied=False):
        div_lat = driver.driver_lat
        div_long = driver.driver_long
        current = sqrt((rest_long-div_long)**2 + (rest_lat-div_lat)**2)
        if current < distance:
            distance = current
            div_id = driver.id
    return div_id



class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    parser_classes = (JSONParser,)

    @detail_route(methods=['post'], url_path='login')
    def login(self, request, pk="r"):
        email = request.data['email']
        password = request.data['password']
        # check the object existing
        rest = get_list_or_404(RestaurantViewSet.queryset, email=email,
                               password=password)
        request.session['id'] = rest[0].id
        return Response(rest[0].getter())

    @detail_route(methods=['delete'], url_path='logout')
    @session_required
    def logout(self, request, pk="r"):
        del request.session['id']
        return Response('Logged out', status=200)

    @detail_route(methods=['get'], url_path='dashboard')
    @session_required
    def dashboard(self, request, pk="r"):
        rest_id = request.session['id']
        rest = get_list_or_404(RestaurantViewSet.queryset, id=rest_id)
        return Response(rest[0].getter())

    @detail_route(methods=['post'], url_path='post')
    @session_required
    def post(self, request, pk='r'):
        rest_id = request.session['id']
        customer_lat = request.data['lat']
        customer_long = request.data['long']
        order_price = request.data['price']
        driver_id = find_driver(rest_id)
        order_obj = Order(restaurant_id=rest_id,
                          driver_id=driver_id, customer_lat=customer_lat,
                          customer_long=customer_long,
                          order_price=order_price, status='S1',)
        order_obj.save()
        return Response(None, status=200)

    @detail_route(methods=['get'], url_path='order')
    @session_required
    def order(self, request, pk='r'):
        rest_id = request.session['id']
        orders = get_list_or_404(Order.objects, restaurant_id=rest_id)
        print(get_list_or_404(Order.objects, restaurant_id=rest_id))
        test = []
        for order in orders:
            test.append(order.getter())
        return Response(test, status=200)


# Create your views here.
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    parser_classes = (JSONParser,)

    @detail_route(methods=['post'], url_path='login')
    def login(self, request, pk="r"):
        email = request.data['email']
        password = request.data['password']
        # check the object existing
        driver = get_list_or_404(DriverViewSet.queryset, email=email,
                                 password=password)
        request.session['id'] = driver[0].id
        return Response(driver[0].getter())

    @detail_route(methods=['delete'], url_path='logout')
    @session_required
    def logout(self, request, pk="r"):
        del request.session['id']
        return Response('Logged out', status=200)

    @detail_route(methods=['get'], url_path='dashboard')
    @session_required
    def dashboard(self, request, pk="r"):
        driver_id = request.session['id']
        driver = get_list_or_404(DriverViewSet.queryset, id=driver_id)
        return Response(driver[0].getter())

    # Get first order
    @detail_route(methods=['get'], url_path='order')
    @session_required
    def order(self, request, pk='r'):
        div_id = request.session['id']
        orders = get_list_or_404(Order.objects, driver_id=div_id)
        return Response(orders[0].getter(), status=200)

    # Order id needed
    # accept the first order or the second
    @detail_route(methods=['post'], url_path='acceptation')
    @session_required
    def acceptation(self, request, pk='r'):
        order_id = request.data['order_id']
        div_id = request.session['id']
        Driver.objects.get(id=div_id).occupied = True
        Order.objects.filter(id=order_id).update(status="S2")
        rest_id = Order.objects.get(id=order_id).restaurant_id
        orders = Order.objects.filter(restaurant_id=rest_id, status='S1')
        orders_accepted = []
        for order in orders:
            orders_accepted.append(order.getter())
        return Response(orders_accepted, status=200)

    # list of orders' id needed
    # Return at most two address and driver's location(index 0)
    @detail_route(methods=['post'], url_path='confirmation')
    @session_required
    def confirmation(self, request, pk='r'):
        orders_id = request.data['order_id']
        customer_address = []
        div_id = request.session['id']
        rest_id = Order.objects.get(id=orders_id[0]).restaurant_id
        div = Driver.objects.get(id=div_id)
        rest = Restaurant.objects.get(id=rest_id)
        div.driver_long = rest.rest_long
        div.driver_lat = rest.rest_lat
        div_location = {'lat': div.driver_long, 'long': div.driver_lat}
        customer_address.append(div_location)
        for order_id in orders_id:
            Order.objects.get(id=order_id).status = "S3"
            location = {'lat': Order.objects.get(id=order_id).customer_lat,
                        'long': Order.objects.get(id=order_id).customer_long}
            customer_address.append(location)

        return Response(customer_address, status=200)

    # to change something when finished one order
    @detail_route(methods=['post'], url_path='delivered')
    @session_required
    def delivered(self, request, pk='r'):
        order_id = request.data['order_id']
        order = Order.objects.get(id=order_id)
        order.status = "S4"
        div_id = request.session['id']
        div = Driver.objects.get(id=div_id)
        div.driver_long = order.customer_long
        div.driver_lat = order.customer_lat
        div.income += order.fee
        rest = Restaurant.objects.get(id=order.restaurant_id)
        rest.income += order.order_price
        if not Order.objects.filter(driver_id=div_id, status='S3').exists():
            div.occupied = False
        return Response("finish an order, good job!", status=200)

# @session_required
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     parser_classes = (JSONParser,)



