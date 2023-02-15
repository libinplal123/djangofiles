from django.urls import path
from . import views

urlpatterns = [
    path('sort_files/', views.sort_files, name='sort_files'),
]