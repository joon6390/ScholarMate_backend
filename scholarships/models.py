from django.db import models

class Scholarship(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    eligibility = models.TextField()  # 신청 자격
    amount = models.CharField(max_length=50)  # 지원 금액
    deadline = models.DateField()  # 신청 마감일

    def __str__(self):
        return self.name
