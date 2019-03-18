from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Driver, Restaurant


admin.site.register(Driver)
admin.site.register(Restaurant)

