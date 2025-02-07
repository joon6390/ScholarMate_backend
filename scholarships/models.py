from django.db import models

class Scholarship(models.Model):
    university_type = models.CharField(max_length=100)  # 대학 유형
    recruitment_start = models.DateField()  # 모집 시작일
    recruitment_end = models.DateField()  # 모집 종료일
    product_id = models.CharField(max_length=50, unique=True)  # 고유 번호
    product_type = models.CharField(max_length=100)  # 장학금 유형
    name = models.CharField(max_length=255)  # 장학금 이름
    selection_method_details = models.TextField(null=True, blank=True)  # 선발 기준 및 절차
    number_of_recipients_details = models.TextField(null=True, blank=True)  # 선발 인원
    grade_criteria_details = models.TextField(null=True, blank=True)  # 성적 기준
    income_criteria_details = models.TextField(null=True, blank=True)  # 소득 기준
    managing_organization_type = models.CharField(max_length=255, null=True, blank=True)  # 운영 기관 구분
    foundation_name = models.CharField(max_length=255, null=True, blank=True)  # 운영 기관 이름
    eligibility_restrictions = models.TextField(null=True, blank=True)  # 자격 제한
    required_documents_details = models.TextField(null=True, blank=True)  # 제출 서류
    residency_requirement_details = models.TextField(null=True, blank=True)  # 지역 조건
    support_details = models.TextField(null=True, blank=True)  # 지원금액
    recommendation_required = models.BooleanField(default=False)  # 추천서 필요 여부
    specific_qualification_details = models.TextField(null=True, blank=True)  # 특정 자격 조건
    major_field_type = models.CharField(max_length=255, null=True, blank=True)  # 학과 구분
    academic_year_type = models.CharField(max_length=255, null=True, blank=True)  # 학년 구분

    def __str__(self):
        return self.name
