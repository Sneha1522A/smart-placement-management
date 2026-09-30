from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'location', 'min_cgpa', 'deadline', 'status', 'created_at')
    list_filter = ('status', 'job_type', 'deadline', 'created_at')
    search_fields = ('title', 'company', 'location', 'eligible_branches', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'deadline'
