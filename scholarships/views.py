from rest_framework import viewsets
from .models import Scholarship
from .serializers import ScholarshipSerializer

class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
