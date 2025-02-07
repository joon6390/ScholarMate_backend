from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

API_URL = "https://api.odcloud.kr/api/15028252/v1/uddi:ccd5ddd5-754a-4eb8-90f0-cb9bce54870b"
SERVICE_KEY = "N3h6qI7uUS8%2Bx3DAbN4CZbI%2Bhmhfg1HUIkzbzMAo4ixWMJ9sOsKwmTB3y1nekc4U%2BIRhKu5vFmagRGznVT8mOw%3D%3D"

class ScholarshipListView(APIView):
    def get(self, request):
        page = int(request.query_params.get("page", 1))  # 현재 페이지
        per_page = int(request.query_params.get("perPage", 10))  # 페이지당 데이터 수
        search_query = request.query_params.get("search", "").replace(" ", "").lower()  # 공백 제거 및 소문자 변환

        all_data = []
        current_page = 1

        while True:
            # 모든 페이지 데이터 가져오기
            request_url = f"{API_URL}?serviceKey={SERVICE_KEY}&page={current_page}&perPage=100&returnType=JSON"
            response = requests.get(request_url)

            if response.status_code != 200 or not response.json().get("data"):
                break

            all_data.extend(response.json().get("data", []))
            current_page += 1

        # 검색어 필터링 (공백 제거 후 비교)
        if search_query:
            all_data = [
                item for item in all_data
                if search_query in item.get("상품명", "").replace(" ", "").lower()
            ]

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
