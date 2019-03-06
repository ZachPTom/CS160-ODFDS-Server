from rest_framework import serializers

from rest_home.models import RestHome

class RestHomeSerializer(serializers.ModelSerializer):
	class Meta:
		model = RestHome
		fields = ['name']