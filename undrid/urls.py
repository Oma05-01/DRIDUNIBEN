from django.urls import path
from . import views

app_name = 'university'

urlpatterns = [
    path('faculties/', views.FacultyListView.as_view(), name='faculty_list'),
    path('faculties/<str:code>/', views.FacultyDetailView.as_view(), name='faculty_detail'),
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/<str:code>/', views.DepartmentDetailView.as_view(), name='department_detail'),
]