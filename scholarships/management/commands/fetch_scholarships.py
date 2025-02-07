import requests
from django.core.management.base import BaseCommand

API_URL = "https://api.odcloud.kr/api/15028252/v1/uddi:ccd5ddd5-754a-4eb8-90f0-cb9bce54870b"
SERVICE_KEY = "N3h6qI7uUS8%2Bx3DAbN4CZbI%2Bhmhfg1HUIkzbzMAo4ixWMJ9sOsKwmTB3y1nekc4U%2BIRhKu5vFmagRGznVT8mOw%3D%3D"

class Command(BaseCommand):
    help = "Fetch scholarship data from the public API and store it in the database"

    def handle(self, *args, **kwargs):
        # API 요청 URL 구성
        request_url = (
            f"{API_URL}?serviceKey={SERVICE_KEY}&page=1&perPage=10&returnType=JSON"
        )

        # API 요청 보내기
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()  # 성공적으로 데이터 받음
            print("Fetched Data:", data)
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
