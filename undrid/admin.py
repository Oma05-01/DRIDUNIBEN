from django.contrib import admin
from .models import Faculty, Department


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department_count')
    search_fields = ('code', 'title')
    inlines = [DepartmentInline]

    def department_count(self, obj):
        return obj.departments.count()

    department_count.short_description = 'Departments'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'faculty')
    list_filter = ('faculty',)
    search_fields = ('code', 'title')
    autocomplete_fields = ('faculty',)