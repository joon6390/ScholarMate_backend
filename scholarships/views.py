from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.permissions import AllowAny
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from .models import Scholarship, Wishlist
from .serializers import WishlistSerializer
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view, permission_classes
from .serializers import CalendarScholarshipSerializer

API_URL = "https://api.odcloud.kr/api/15028252/v1/uddi:ccd5ddd5-754a-4eb8-90f0-cb9bce54870b"
SERVICE_KEY = "N3h6qI7uUS8%2Bx3DAbN4CZbI%2Bhmhfg1HUIkzbzMAo4ixWMJ9sOsKwmTB3y1nekc4U%2BIRhKu5vFmagRGznVT8mOw%3D%3D"

class ScholarshipListView(APIView):
    permission_classes = [AllowAny]  # ✅ 인증 없이 접근 가능

    def get(self, request):
        page = int(request.query_params.get("page", 1))  # 현재 페이지
        per_page = int(request.query_params.get("perPage", 10))  # 페이지당 데이터 수
        search_query = request.query_params.get("search", "").replace(" ", "").lower()  # 검색어 처리
        selected_type = request.query_params.get("type", "")  # 🔥 장학금 유형 필터
        sort_order = request.query_params.get("sort", "")  # 정렬 옵션

        all_data = []
        current_page = 1

        while True:
            # 전체 페이지의 데이터를 가져오기 위해 루프 실행
            request_url = f"{API_URL}?serviceKey={SERVICE_KEY}&page={current_page}&perPage=100&returnType=JSON"
            response = requests.get(request_url)

            if response.status_code != 200 or not response.json().get("data"):
                break  # 더 이상 데이터가 없으면 중단

            all_data.extend(response.json().get("data", []))
            current_page += 1

        # 🔹 검색어 필터링 (공백 제거 후 비교)
        if search_query:
            all_data = [
                item for item in all_data
                if search_query in item.get("상품명", "").replace(" ", "").lower()
            ]

        # 🔥 장학금 유형 필터링 (학자금유형구분 필드 기반)
        if selected_type:
            all_data = [item for item in all_data if item.get("학자금유형구분", "") == selected_type]

        # 🔥 모집 종료일 기준 정렬 (정렬 옵션이 "end_date"인 경우)
        if sort_order == "end_date":
            def parse_date(date_str):
                """ 날짜를 YYYY-MM-DD 형식으로 변환하고, 변환 실패 시 큰 값 반환 """
                try:
                    return datetime.strptime(date_str, "%Y-%m-%d")  # 날짜 변환
                except (ValueError, TypeError):  # 날짜가 없거나 잘못된 형식일 경우
                    return datetime.max  # 가장 늦은 날짜로 처리하여 정렬에서 마지막으로 위치

            all_data.sort(key=lambda x: parse_date(x.get("모집종료일", "")))  # 모집 종료일 기준 정렬

        # 페이지네이션 적용
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = all_data[start_index:end_index]

        return Response(
            {
                "data": paginated_data,  # 현재 페이지 데이터
                "total": len(all_data),  # 검색된 데이터 개수
            },
            status=status.HTTP_200_OK,
        )

class ToggleWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        action = request.data.get("action")
        product_id = request.data.get("product_id")

        if action == "remove" and product_id:
            scholarship = get_object_or_404(Scholarship, product_id=product_id)
            Wishlist.objects.filter(user=request.user, scholarship=scholarship).delete()
            return Response({"status": "removed"})

        scholarship_id = request.data.get("scholarship_id")
        if not scholarship_id:
            return Response({"error": "scholarship_id 필요"}, status=400)

        scholarship = get_object_or_404(Scholarship, id=scholarship_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, scholarship=scholarship)
        if not created:
            wishlist.delete()
            return Response({"status": "removed"})
        return Response({"status": "added"})

class UserWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)

class AddToWishlistFromAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        name = data.get("상품명")
        foundation = data.get("운영기관명")
        product_id = f"{name}_{foundation}"

        scholarship, _ = Scholarship.objects.get_or_create(
            product_id=product_id,
            defaults={
                "name": name,
                "foundation_name": foundation,
                "recruitment_start": parse_date(data.get("모집시작일")),
                "recruitment_end": parse_date(data.get("모집종료일")),
                "university_type": data.get("대학구분", ""),
                "product_type": data.get("학자금유형구분", ""),
                "grade_criteria_details": data.get("성적기준 상세내용", ""),
                "income_criteria_details": data.get("소득기준 상세내용", ""),
                "support_details": data.get("지원내역 상세내용", ""),
                "specific_qualification_details": data.get("특정자격 상세내용", ""),
                "residency_requirement_details": data.get("지역거주여부 상세내용", ""),
                "selection_method_details": data.get("선발방법 상세내용", ""),
                "number_of_recipients_details": data.get("선발인원 상세내용", ""),
                "eligibility_restrictions": data.get("자격제한 상세내용", ""),
                "required_documents_details": data.get("제출서류 상세내용", ""),
                "recommendation_required": data.get("추천필요여부 상세내용", "") == "필요",
                "major_field_type": data.get("계열구분", ""),
                "academic_year_type": data.get("학년구분", ""),
                "managing_organization_type": data.get("운영기관구분", ""),
            }
        )

        wishlist, created = Wishlist.objects.get_or_create(user=request.user, scholarship=scholarship)
        return Response({"status": "added" if created else "exists"})
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, pk):
    try:
        wishlist = Wishlist.objects.get(user=request.user, scholarship__id=pk)
        wishlist.delete()
        return Response({"status": "deleted"}, status=200)
    except Wishlist.DoesNotExist:
        return Response({"error": "해당 장학금이 관심 목록에 없습니다."}, status=404)
    
class MyCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlisted = Wishlist.objects.filter(user=request.user)
        serializer = CalendarScholarshipSerializer(wishlisted, many=True)
        return Response(serializer.data)
    
