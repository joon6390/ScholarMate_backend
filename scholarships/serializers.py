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

class CalendarScholarshipSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='scholarship.name')
    deadline = serializers.DateField(source='scholarship.recruitment_end')
    documents = serializers.CharField(source='scholarship.required_documents_details')

    class Meta:
        model = Wishlist
        fields = ['id', 'title', 'deadline', 'documents']