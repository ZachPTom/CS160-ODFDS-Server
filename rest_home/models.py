from django.db import models


# Create your models here.
class RestHome(models.Model):
	costumer_name = models.CharField(max_length=200)
	costumer_phone = models.CharField(max_length=100)
	costumer_address = models.CharField(max_length=200)
	food = models.CharField(max_length=300)
	order_placed_date_time = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.costumer_name 