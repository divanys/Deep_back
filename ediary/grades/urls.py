from django.urls import path
from . import views

urlpatterns = [
    path('lesson/<int:load_id>/', views.lesson_management, name='lesson_management'),
]