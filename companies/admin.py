from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Company model.
    """
    list_display = ('name', 'job_role', 'package_lpa', 'min_cgpa', 'deadline', 'created_at')
    list_filter = ('deadline',)
    search_fields = ('name', 'job_role')
    ordering = ('deadline', 'name')
