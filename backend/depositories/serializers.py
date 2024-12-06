from rest_framework import serializers
from .models import Depository 


class DepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Depository 
        fields = '__all__'

