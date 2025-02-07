from django.contrib import admin
from .models import Scholarship


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'foundation_name', 'recruitment_start', 'recruitment_end')
    search_fields = ('name', 'foundation_name')
