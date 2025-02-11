from rest_framework import generics
from .models import Myinfor
from .serializers import MyinforSerializer
from rest_framework.permissions import IsAuthenticated

class MyinforCreateView(generics.CreateAPIView):
    queryset = Myinfor.objects.all()
    serializer_class = MyinforSerializer
    permission_classes = [IsAuthenticated]
