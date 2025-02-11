from django.urls import path
from .views import MyinforCreateView

urlpatterns = [
    path('register-info/', MyinforCreateView.as_view(), name='register-info'),
]
