from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Faculty, Department


class FacultyListView(ListView):
    model = Faculty
    template_name = 'university/faculty_list.html'
    context_object_name = 'faculties'


class FacultyDetailView(DetailView):
    model = Faculty
    template_name = 'university/faculty_detail.html'
    context_object_name = 'faculty'
    pk_url_kwarg = 'code'

    def get_object(self):
        return get_object_or_404(Faculty, pk=self.kwargs['code'])


class DepartmentListView(ListView):
    model = Department
    template_name = 'university/department_list.html'
    context_object_name = 'departments'


class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'university/department_detail.html'
    context_object_name = 'department'
    pk_url_kwarg = 'code'

    def get_object(self):
        return get_object_or_404(Department, pk=self.kwargs['code'])