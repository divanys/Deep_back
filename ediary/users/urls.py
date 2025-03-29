from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('auth/', views.auth, name='auth'),
    # path('prep_curator/', views.prep_curator, name='prep_curator'),
    # path("prep_curator/groups/", views.list_groups, name="list_groups"),
    # path('prep_discipline/', views.prep_discipline, name='prep_discipline'),
    # path('student/', views.student, name='student'),
    # path('parent/', views.parent, name='parent'),
    # path('admin/', views.admin, name='admin'),
    path('students/student_list/', views.student_list, name='student_list'),
]
