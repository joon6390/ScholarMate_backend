from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("auth/", include("djoser.urls")),  # 회원가입, 회원정보 조회
    path("auth/", include("djoser.urls.jwt")),  # JWT 로그인, 로그아웃
    path('admin/', admin.site.urls),
    path('scholarships/', include('scholarships.urls')),  # scholarships 앱 URL 포함
]
