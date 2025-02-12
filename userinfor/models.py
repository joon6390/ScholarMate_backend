from django.db import models
from django.contrib.auth.models import User

class UserScholarship(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # 사용자 1명당 1개의 장학 정보
    name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    income_level = models.CharField(max_length=50, null=True, blank=True)
    university_category = models.CharField(max_length=50, null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    academic_year = models.CharField(max_length=20, null=True, blank=True)
    semester = models.CharField(max_length=20, null=True, blank=True)
    gpa_last = models.FloatField(null=True, blank=True)
    gpa_total = models.FloatField(null=True, blank=True)
    multi_culture_family = models.BooleanField(default=False)
    single_parent_family = models.BooleanField(default=False)
    multiple_children_family = models.BooleanField(default=False)
    national_merit = models.BooleanField(default=False)
    additional_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - 장학 정보"
