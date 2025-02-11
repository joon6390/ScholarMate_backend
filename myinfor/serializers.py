from rest_framework import serializers
from .models import Myinfor

class MyinforSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myinfor
        fields = '__all__'
