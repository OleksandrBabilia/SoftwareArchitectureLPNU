from rest_framework import serializers
from .models import Book, Ganre 


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book 
        fields = '__all__'


class GanreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ganre 
        fields = '__all__'

