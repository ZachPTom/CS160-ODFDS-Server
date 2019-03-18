from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Driver(models.Model):
    # login information
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    phone = models.BigIntegerField(unique=True, validators=[
        MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    # other information
    time_joined = models.DateField(auto_now_add=True)
    ssn = models.IntegerField(unique=True, validators=[
        MaxValueValidator(999999999), MinValueValidator(100000000)])
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    income = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    car_plate = models.CharField(max_length=10)
    car_model = models.CharField(max_length=20)
    location = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Restaurant(models.Model):
    # login information
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    phone = models.BigIntegerField(unique=True, validators=[
        MaxValueValidator(9999999999), MinValueValidator(1000000000)])
    # other information
    time_joined = models.DateField(auto_now_add=True)
    restaurant_name = models.CharField(max_length=50)
    income = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    address = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.restaurant_name
