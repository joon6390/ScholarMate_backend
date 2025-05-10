from django.core.management.base import BaseCommand
from scholarships.models import Scholarship
import requests
from datetime import datetime

API_URL = "https://api.odcloud.kr/api/15028252/v1/uddi:ccd5ddd5-754a-4eb8-90f0-cb9bce54870b"
SERVICE_KEY = "N3h6qI7uUS8%2Bx3DAbN4CZbI%2Bhmhfg1HUIkzbzMAo4ixWMJ9sOsKwmTB3y1nekc4U%2BIRhKu5vFmagRGznVT8mOw%3D%3D"

class Command(BaseCommand):
    help = "공공 API에서 장학금 정보를 가져와 DB에 저장"

    def handle(self, *args, **options):
        page = 1
        count = 0

        while True:
            url = f"{API_URL}?serviceKey={SERVICE_KEY}&page={page}&perPage=100&returnType=JSON"
            response = requests.get(url)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"API 요청 실패: {response.status_code}"))
                break

            data = response.json().get("data", [])
            if not data:
                break

            for item in data:
                product_name = item.get("상품명", "").strip()
                org_name = item.get("운영기관명", "").strip()
                if not product_name or not org_name:
                    continue

                product_id = f"{product_name}_{org_name}"

                if Scholarship.objects.filter(product_id=product_id).exists():
                    continue

                try:
                    Scholarship.objects.create(
                        product_id=product_id,
                        name=product_name,
                        foundation_name=org_name,
                        recruitment_start=self.safe_parse_date(item.get("모집시작일")),
                        recruitment_end=self.safe_parse_date(item.get("모집종료일")),
                        university_type=item.get("대학구분", ""),
                        product_type=item.get("학자금유형구분", ""),
                        grade_criteria_details=item.get("성적기준 상세내용", ""),
                        income_criteria_details=item.get("소득기준 상세내용", ""),
                        support_details=item.get("지원내역 상세내용", ""),
                        specific_qualification_details=item.get("특정자격 상세내용", ""),
                        residency_requirement_details=item.get("지역거주여부 상세내용", ""),
                        selection_method_details=item.get("선발방법 상세내용", ""),
                        number_of_recipients_details=item.get("선발인원 상세내용", ""),
                        eligibility_restrictions=item.get("자격제한 상세내용", ""),
                        required_documents_details=item.get("제출서류 상세내용", ""),
                        recommendation_required=item.get("추천필요여부 상세내용", "") == "필요",
                        major_field_type=item.get("계열구분", ""),
                        academic_year_type=item.get("학년구분", ""),
                        managing_organization_type=item.get("운영기관구분", ""),
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"❌ 저장 중 오류 발생: {e}"))

            page += 1

        self.stdout.write(self.style.SUCCESS(f"{count}개의 장학금이 저장되었습니다."))

    def safe_parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            return None
