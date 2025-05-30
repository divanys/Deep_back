from django.urls import path
from .views import student_info, curator_info, teacher_info
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('auth/', views.auth, name='auth'),
    path('students/student_list/', views.student_list, name='student_list'),
    path("students/info/", student_info),
    path("admin/import_discipline_prepods/", teacher_info, name="import_discipline_prepods"),
    path("admin/import_tutor_prepods/", curator_info, name="import_tutor_prepods"),
    path("curators/info/", curator_info, name="curator_info"),
    path("teacher/info/", teacher_info, name="teacher_info"),
]

