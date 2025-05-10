from rest_framework import serializers
from .models import Wishlist, Scholarship

class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    scholarship = ScholarshipSerializer()

    class Meta:
        model = Wishlist
        fields = ['id', 'scholarship', 'added_at']