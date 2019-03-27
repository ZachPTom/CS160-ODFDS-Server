from rest_framework import serializers

from rest_home.models import RestHome

class RestHomeSerializer(serializers.ModelSerializer):
	class Meta:
		model = RestHome
		fields = ['costumer_name', 'costumer_phone', 'costumer_address', 'food', 'order_placed_date_time']