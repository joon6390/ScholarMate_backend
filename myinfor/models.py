from django.db import models
from django.contrib.auth.models import User

class Myinfor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    univ_category = models.CharField(max_length=50, choices=[
        ('4년제', '4년제(5-6년제 포함)'),
        ('전문대', '전문대(2-3년제)'),
        ('해외대학', '해외대학')
    ])
    gender = models.CharField(max_length=10, choices=[
        ('남성', '남성'),
        ('여성', '여성'),
        ('선택안함', '선택안함')
    ])
    age = models.PositiveIntegerField()
    university = models.CharField(max_length=100)
    semester = models.CharField(max_length=50, choices=[
        ('대학 신입생', '대학 신입생'),
        ('대학 1학기', '대학 1학기'),
        ('대학 2학기', '대학 2학기'),
        ('대학 8학기 이상', '대학 8학기 이상')
    ])
    major_category = models.CharField(max_length=50)
    major = models.CharField(max_length=100)
    totalGPA = models.FloatField()
    income = models.IntegerField()
    residence = models.CharField(max_length=150)
    etc = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.university}"
