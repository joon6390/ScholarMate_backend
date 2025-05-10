from django.urls import path
from .views import (
    ScholarshipListView,
    ToggleWishlistAPIView,
    UserWishlistAPIView,
    AddToWishlistFromAPI,
    remove_from_wishlist,  
    MyCalendarView,
)

urlpatterns = [
    path('api/scholarships/', ScholarshipListView.as_view(), name='scholarship-list'),
    path('api/wishlist/toggle/', ToggleWishlistAPIView.as_view(), name='wishlist-toggle'),
    path('api/wishlist/', UserWishlistAPIView.as_view(), name='wishlist-list'),
    path('api/wishlist/add-from-api/', AddToWishlistFromAPI.as_view(), name='wishlist-add-from-api'),  # ✅ 이 줄 추가
    path('api/wishlist/delete/<int:pk>/', remove_from_wishlist, name='wishlist-delete'),
    path("calendar/", MyCalendarView.as_view(), name="my-calendar"),
]
