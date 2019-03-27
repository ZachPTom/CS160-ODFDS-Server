from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Driver(models.Model):
    # login information
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    #phone = models.BigIntegerField(unique=True, validators=[
    #    MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    # other information
    #time_joined = models.DateField(auto_now_add=True)
    #ssn = models.IntegerField(unique=True, validators=[
    #    MaxValueValidator(999999999), MinValueValidator(100000000)])
    #date_of_birth = models.DateField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    income = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    #car_plate = models.CharField(max_length=10)
    #car_model = models.CharField(max_length=20)
    driver_lat = models.FloatField(default=-1, validators=[
        MaxValueValidator(90), MinValueValidator(-1)])
    driver_long = models.FloatField(default=-1, validators=[
        MaxValueValidator(180), MinValueValidator(-1)])
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def getter(self):
        return {
            "email": self.email,
            #"phone": self.phone,
            #"time_joined": self.time_joined,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "income": self.income,
            #"car_plate": self.car_plate,
            #"car_model": self.car_model,
            "location": [self.driver_lat, self.driver_long]
        }


class Restaurant(models.Model):
    # login information
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    #phone = models.BigIntegerField(unique=True, validators=[
    #    MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    # other information
    time_joined = models.DateField(auto_now_add=True)
    restaurant_name = models.CharField(max_length=50)
    income = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    rest_lat = models.FloatField(default=-1, validators=[
        MaxValueValidator(90), MinValueValidator(-1)])
    rest_long = models.FloatField(default=-1, validators=[
        MaxValueValidator(180), MinValueValidator(-1)])

    def __str__(self):
        return self.restaurant_name

    def getter(self):
        return {"email": self.email,
                #"phone": self.phone,
                "time_joined": self.time_joined,
                "restaurant_name": self.restaurant_name,
                "income": self.income,
                "address": [self.rest_lat, self.rest_long]}


class Order(models.Model):
    restaurant_id = models.SmallIntegerField(default=-1)
    driver_id = models.SmallIntegerField(default=-1)
    customer_lat = models.FloatField(default=-1, validators=[
        MaxValueValidator(90), MinValueValidator(-1)])
    customer_long = models.FloatField(default=-1, validators=[
        MaxValueValidator(180), MinValueValidator(-1)])
    order_price = models.FloatField(default=0)
    fee = models.FloatField(default=0)
    STEP1 = 'S1'
    STEP2 = 'S2'
    STEP3 = 'S3'
    STEP4 = 'S4'
    ORDER_PROCESS = (
        (STEP1, 'Looking drivers'),
        (STEP2, 'Waiting pick up'),
        (STEP3, 'Sending an order'),
        (STEP4, 'delivered'),
    )
    status = models.CharField(
        max_length=2,
        choices=ORDER_PROCESS,
        default=STEP1,
    )

    def __str__(self):
        return str(self.id)

    def getter(self):
        return {"id": self.id,
                "customer_lat": self.customer_long,
                "status": self.status,
                "total_price": self.order_price+self.fee,
                "address": [self.customer_lat, self.customer_long]}





