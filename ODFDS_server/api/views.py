from api.models import Driver, Restaurant, Order, Token
from api.serializers import DriverSerializer, RestaurantSerializer
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from functools import wraps
import googlemaps
import secrets


def duration(origin, destination):
    gmaps = googlemaps.Client(key='AIzaSyDBmKH8_o35KRFWmcke2WO8xddSSvzT_-8')
    directions_result = gmaps.distance_matrix(origin, destination,
                                              mode='driving')
    if type(destination) is list:
        return float(directions_result['rows'][0]['elements'][0]['duration']
                ['value']) + float(directions_result['rows'][0]['elements'][1]
                ['duration']['value'])
    return float(directions_result['rows'][0]['elements'][0]['duration'][
                    'value'])


def order_sort(location):
    first_order_first = duration({'lat': location['rest'][0],
                                  'lng': location['rest'][1]},
                                 [{'lat': location['first'][0],
                                   'lng':location['first'][1]},
                                  {'lat': location['second'][0],
                                   'lng': location['second'][1]}])

    second_order_first = duration({'lat': location['rest'][0],
                                  'lng': location['rest'][1]},
                                  [{'lat': location['second'][0],
                                   'lng':location['second'][1]},
                                  {'lat': location['first'][0],
                                   'lng': location['first'][1]}])
    if first_order_first <= second_order_first:
        return location
    else:
        location['first'], location['second'] = location['second'], location[
            'first']
        return location


def fee_computation(rest_id, destination):
    rest_lat = Restaurant.objects.get(id=rest_id).rest_lat
    rest_long = Restaurant.objects.get(id=rest_id).rest_long
    rest_location = {'lat': rest_lat, 'lng': rest_long}
    gmaps = googlemaps.Client(key='AIzaSyDBmKH8_o35KRFWmcke2WO8xddSSvzT_-8')
    directions_result = gmaps.distance_matrix(rest_location, destination,
                                              units='imperial', mode='driving')
    miles = float(directions_result['rows'][0]['elements'][0]['distance']
                  ['text'][:-3])
    return driver_fee(miles)


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        num_result = Token.objects.filter(keys=args[1].data.get('key',
                                                                None)).count()
        if not num_result:
            return HttpResponse('Not logged in', status=401)
        return f(*args, **kwargs)
    return wrapper


def find_driver(rest_id):
    rest_lat = Restaurant.objects.get(id=rest_id).rest_lat
    rest_long = Restaurant.objects.get(id=rest_id).rest_long
    # a day
    max_time = 86400
    for driver in Driver.objects.filter(occupied=False):
        div_lat = driver.driver_lat
        div_long = driver.driver_long
        current = duration({'lat': div_lat, 'lng': div_long}, {'lat':
                                    rest_lat, 'lng': rest_long})
        if current < max_time:
            max_time = current
            div_id = driver.id
    if max_time != 86400:
        return div_id
    else:
        find_driver(rest_id)


def second_orders_filter(orders, first_order):
    rest_id = Order.objects.get(id=first_order).restaurant_id
    rest_lat = Restaurant.objects.get(id=rest_id).rest_lat
    rest_long = Restaurant.objects.get(id=rest_id).rest_long
    first_lat = Order.objects.get(id=first_order).customer_lat
    first_long = Order.objects.get(id=first_order).customer_long
    driver_id = Order.objects.get(id=first_order).driver_id
    driver_lat = Driver.objects.get(id=driver_id).driver_lat
    driver_long = Driver.objects.get(id=driver_id).driver_long
    first_time = duration({'lat': rest_lat, 'lng': rest_long},
                       {'lat': first_lat, 'lng': first_long})
    first_time = first_time + duration({'lat': driver_lat, 'lng': driver_long},
                       {'lat': rest_lat, 'lng': rest_long})
    if first_time > 1800:
        orders.clear()
        return
    for order in orders:
        first_order_first = duration({'lat': rest_lat, 'lng': rest_long},
                    [{'lat': first_lat, 'lng': first_long},
                    {'lat': order['address'][0], 'lng': order['address'][1]}])
        second_order_first = duration({'lat': rest_lat, 'lng': rest_long},
                    [{'lat': order['address'][0], 'lng': order['address'][1]},
                    {'lat': first_lat, 'lng': first_long}])

        if first_order_first <= second_order_first:
            total_time = first_order_first
        else:
            total_time = second_order_first
        if total_time > 2400:
            orders.remove(order)
    return


def driver_fee(miles):
    if miles <= 1:
        return 6
    elif miles <= 2:
        return 8
    else:
        return 6 + round(miles - 1) * 2


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    parser_classes = (JSONParser,)

    @detail_route(methods=['post'], url_path='login')
    def login(self, request, pk="r"):
        email = request.data['email']
        password = request.data['password']
        rest = get_list_or_404(RestaurantViewSet.queryset, email=email,
                               password=password)
        key = secrets.token_hex(16)
        num = Restaurant.objects.get(email=rest[0].getter()['email']).id
        token = Token(keys=key, user_id=num)
        token.save()
        user_info = rest[0].getter()
        user_info['key'] = key
        return Response(user_info, status=200)

    @detail_route(methods=['delete'], url_path='logout')
    @token_required
    def logout(self, request, pk="r"):
        Token.objects.filter(keys=request.data['key']).delete()
        return Response(status=200)

    @detail_route(methods=['post'], url_path='dashboard')
    @token_required
    def dashboard(self, request, pk="r"):
        rest_id = Token.objects.get(keys=request.data['key']).user_id
        rest = get_list_or_404(RestaurantViewSet.queryset, id=rest_id)
        return Response(rest[0].getter())

    @detail_route(methods=['post'], url_path='route')
    @token_required
    def route(self, request, pk='r'):
        first_id = request.data['order_id']
        first_lat = Order.objects.get(id=first_id).customer_lat
        first_long = Order.objects.get(id=first_id).customer_long
        rest_id = Order.objects.get(id=first_id).restaurant_id
        rest_lat = Restaurant.objects.get(id=rest_id).rest_lat
        rest_long = Restaurant.objects.get(id=rest_id).rest_long
        driver_id = Order.objects.get(id=first_id).driver_id
        driver_lat = Driver.objects.get(id=driver_id).driver_lat
        driver_long = Driver.objects.get(id=driver_id).driver_long
        order_List = []
        for order in Order.objects.filter(driver_id=driver_id, status='S3'):
            order_List.append(order.getter())
        if len(order_List) == 2:
            for order in order_List:
                if order['id'] == first_id:
                    order_List.remove(order)
            second_order = order_List[0]
            second_lat = second_order['address'][0]
            second_long = second_order['address'][1]
            location = {'rest': [rest_lat, rest_long],
                        "driver": [driver_lat, driver_long],
                        'first': [first_lat, first_long],
                        'second': [second_lat, second_long]}
            location = order_sort(location)
            if location['first'][0] != first_lat or location['first'][1] != first_long:
                return Response(location, status=200)
        return Response({'rest': [rest_lat, rest_long],
                         "driver": [driver_lat, driver_long],
                         'first': [first_lat, first_long]}, status=200)

    @detail_route(methods=['post'], url_path='post')
    @token_required
    def post(self, request, pk='r'):
        rest_id = Token.objects.get(keys=request.data['key']).user_id
        customer_lat = request.data['lat']
        customer_long = request.data['long']
        order_price = request.data['price']
        driver_id = find_driver(rest_id)
        fee = fee_computation(rest_id, {'lat': customer_lat,
                                        'lng': customer_long})
        order_obj = Order(restaurant_id=rest_id,
                          driver_id=driver_id, customer_lat=customer_lat,
                          customer_long=customer_long,
                          order_price=order_price,
                          fee=fee)
        order_obj.save()
        return Response(status=200)

    @detail_route(methods=['post'], url_path='order')
    @token_required
    def order(self, request, pk='r'):
        rest_id = Token.objects.get(keys=request.data['key']).user_id
        orders = get_list_or_404(Order.objects, restaurant_id=rest_id)
        order_List = []
        for order in orders:
            order_List.append(order.getter())
        return Response(order_List, status=200)


# Create your views here.
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    parser_classes = (JSONParser,)

    @detail_route(methods=['post'], url_path='login')
    def login(self, request, pk="r"):
        email = request.data['email']
        password = request.data['password']
        driver = get_list_or_404(DriverViewSet.queryset, email=email,
                                 password=password)
        key = secrets.token_hex(16)
        num = Driver.objects.get(email=driver[0].getter()['email']).id
        token = Token(keys=key, user_id=num)
        token.save()
        user_info = driver[0].getter()
        user_info['key'] = key
        return Response(user_info, status=200)

    @detail_route(methods=['delete'], url_path='logout')
    @token_required
    def logout(self, request, pk="r"):
        Token.objects.filter(keys=request.data['key']).delete()
        return Response(status=200)

    @detail_route(methods=['post'], url_path='dashboard')
    @token_required
    def dashboard(self, request, pk="r"):
        driver_id = Token.objects.get(keys=request.data['key']).user_id
        driver = get_list_or_404(DriverViewSet.queryset, id=driver_id)
        return Response(driver[0].getter())

    # Get first order
    @detail_route(methods=['post'], url_path='order')
    @token_required
    def order(self, request, pk='r'):
        div_id = Token.objects.get(keys=request.data['key']).user_id
        orders = get_list_or_404(Order.objects, driver_id=div_id, status='S1')
        order_List = []
        for order in orders:
            this_order = order.getter()
            rest = Restaurant.objects.get(id=this_order['rest'])
            rest_address = [rest.rest_lat, rest.rest_long]
            this_order['rest_address'] = rest_address
            this_order['rest'] = rest.restaurant_name
            order_List.append(this_order)
        return Response(order_List, status=200)

    # Order id needed
    # accept the first order or the second
    @detail_route(methods=['post'], url_path='first_acceptation')
    @token_required
    def first_acceptation(self, request, pk='r'):
        order_id = request.data['order_id']
        div_id = Token.objects.get(keys=request.data['key']).user_id
        Driver.objects.filter(id=div_id).update(occupied=True)
        Order.objects.filter(id=order_id).update(status="S2")
        rest_id = Order.objects.get(id=order_id).restaurant_id
        orders = Order.objects.filter(restaurant_id=rest_id, status='S1')
        second_orders = []
        for order in orders:
            second_orders.append(order.getter())
        second_orders_filter(second_orders, order_id)
        return Response(second_orders, status=200)

    @detail_route(methods=['post'], url_path='second_acceptation')
    @token_required
    def second_acceptation(self, request, pk='r'):
        order_id = request.data['order_id']
        div_id = Token.objects.get(keys=request.data['key']).user_id
        Order.objects.filter(id=order_id).update(status="S2")
        Order.objects.filter(id=order_id).update(driver_id=div_id)
        return Response(status=200)

    # the first order always delivery first
    @detail_route(methods=['post'], url_path='route')
    @token_required
    def route(self, request, pk='r'):
        first_id = request.data['first_id']
        first_lat = Order.objects.get(id=first_id).customer_lat
        first_long = Order.objects.get(id=first_id).customer_long
        rest_id = Order.objects.get(id=first_id).restaurant_id
        rest_lat = Restaurant.objects.get(id=rest_id).rest_lat
        rest_long = Restaurant.objects.get(id=rest_id).rest_long
        driver_id = Order.objects.get(id=first_id).driver_id
        driver_lat = Driver.objects.get(id=driver_id).driver_lat
        driver_long = Driver.objects.get(id=driver_id).driver_long
        if request.data['second_id']:
            second_id = request.data['second_id']
            second_lat = Order.objects.get(id=second_id).customer_lat
            second_long = Order.objects.get(id=second_id).customer_long
            two_orders = order_sort({'rest': [rest_lat, rest_long],
                             "driver": [driver_lat, driver_long],
                             'first': [first_lat, first_long],
                             'second': [second_lat, second_long]})
            return Response(two_orders, status=200)
        return Response({'rest': [rest_lat, rest_long],
                         "driver": [driver_lat, driver_long],
                         'first': [first_lat, first_long]}, status=200)

    @detail_route(methods=['post'], url_path='update')
    @token_required
    def update_driver(self, request, pk='r'):
        driver_id = Token.objects.get(keys=request.data['key']).user_id
        driver_lat = request.data['driver_lat']
        driver_long = request.data['driver_long']
        Driver.objects.filter(id=driver_id).update(driver_lat=driver_lat)
        Driver.objects.filter(id=driver_id).update(driver_long=driver_long)
        return Response(status=200)

    # list of orders' id needed
    # Return at most two address and driver's location(index 0)
    @detail_route(methods=['post'], url_path='confirmation')
    @token_required
    def confirmation(self, request, pk='r'):
        orders_id = request.data['order_id']
        div_id = Token.objects.get(keys=request.data['key']).user_id
        rest_id = Order.objects.get(id=orders_id[0]).restaurant_id
        div = Driver.objects.filter(id=div_id)
        rest = Restaurant.objects.get(id=rest_id)
        div.update(driver_long=rest.rest_long)
        div.update(driver_lat=rest.rest_lat)
        for order_id in orders_id:
            Order.objects.filter(id=order_id).update(status="S3")
        return Response(status=200)

    @detail_route(methods=['post'], url_path='delivered')
    @token_required
    def delivered(self, request, pk='r'):
        order_id = request.data['order_id']
        order = Order.objects.filter(id=order_id)
        order_info = Order.objects.get(id=order_id)
        order.update(status="S4")
        div_id = Token.objects.get(keys=request.data['key']).user_id
        div_info = Driver.objects.get(id=div_id)
        div = Driver.objects.filter(id=div_id)
        div.update(driver_long=order_info.customer_long)
        div.update(driver_lat=order_info.customer_lat)
        div.update(income=div_info.income + order_info.fee)
        rest = Restaurant.objects.filter(id=order_info.restaurant_id)
        rest_info = Restaurant.objects.get(id=order_info.restaurant_id)
        rest.update(income=order_info.order_price + rest_info.income)
        if not Order.objects.filter(driver_id=div_id, status='S3').exists():
            div.update(occupied=False)
        return Response(status=200)




