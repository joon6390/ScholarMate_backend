from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserScholarship
from .serializers import UserScholarshipSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_scholarship_info(request):
    user = request.user
    data = request.data

    # 기존 정보가 있으면 업데이트, 없으면 생성
    scholarship_info, created = UserScholarship.objects.get_or_create(user=user)

    scholarship_info.name = data.get("name", scholarship_info.name)
    scholarship_info.gender = data.get("gender", scholarship_info.gender)
    scholarship_info.birth_date = data.get("birth_date", scholarship_info.birth_date)
    scholarship_info.region = data.get("region", scholarship_info.region)
    scholarship_info.district = data.get("district", scholarship_info.district)
    scholarship_info.income_level = data.get("income_level", scholarship_info.income_level)
    scholarship_info.university_category = data.get("university_category", scholarship_info.university_category)
    scholarship_info.university = data.get("university", scholarship_info.university)
    scholarship_info.department = data.get("department", scholarship_info.department)
    scholarship_info.academic_year = data.get("academic_year", scholarship_info.academic_year)
    scholarship_info.semester = data.get("semester", scholarship_info.semester)
    scholarship_info.gpa_last = data.get("gpa_last", scholarship_info.gpa_last)
    scholarship_info.gpa_total = data.get("gpa_total", scholarship_info.gpa_total)
    scholarship_info.multi_culture_family = data.get("multi_culture_family", scholarship_info.multi_culture_family)
    scholarship_info.single_parent_family = data.get("single_parent_family", scholarship_info.single_parent_family)
    scholarship_info.multiple_children_family = data.get("multiple_children_family", scholarship_info.multiple_children_family)
    scholarship_info.national_merit = data.get("national_merit", scholarship_info.national_merit)
    scholarship_info.additional_info = data.get("additional_info", scholarship_info.additional_info)

    scholarship_info.save()
    
    return Response({"message": "장학 정보가 저장되었습니다."})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_scholarship_info(request):
    user = request.user
    try:
        scholarship_info = UserScholarship.objects.get(user=user)
        serializer = UserScholarshipSerializer(scholarship_info)
        return Response(serializer.data)
    except UserScholarship.DoesNotExist:
        return Response({"message": "장학 정보가 없습니다."}, status=404)
