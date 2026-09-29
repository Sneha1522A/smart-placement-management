from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    # List all companies
    path('', views.company_list, name='company_list'),
    
    # Add a company
    path('add/', views.company_create, name='company_create'),
    
    # Edit a company
    path('<int:pk>/edit/', views.company_update, name='company_update'),
    
    # Delete a company
    path('<int:pk>/delete/', views.company_delete, name='company_delete'),
]
