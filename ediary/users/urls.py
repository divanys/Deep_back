from django.urls import path
from .views import student_info, curator_info, teacher_info
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('auth/', views.auth, name='auth'),
    # path('prep_curator/', views.prep_curator, name='prep_curator'),
    # path("prep_curator/groups/", views.list_groups, name="list_groups"),
    # path('prep_discipline/', views.prep_discipline, name='prep_discipline'),
    # path('student/', views.student, name='student'),
    # path('parent/', views.parent, name='parent'),
    path('students/student_list/', views.student_list, name='student_list'),
    path("students/info/", student_info),
    path("admin/import_discipline_prepods/", teacher_info, name="import_discipline_prepods"),
    path("admin/import_tutor_prepods/", curator_info, name="import_tutor_prepods"),
    path("curators/info/", curator_info, name="curator_info"),
    path("teacher/info/", teacher_info, name="teacher_info"),
]

