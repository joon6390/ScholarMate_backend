from django.urls import path
from .views import ScholarshipListView

urlpatterns = [
    path("api/scholarships/", ScholarshipListView.as_view(), name="scholarship-list"),
]
