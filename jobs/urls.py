from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_management, name='job_management'),
]
