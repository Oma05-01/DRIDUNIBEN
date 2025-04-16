from django.contrib import admin
from . models import *
from bson.objectid import ObjectId
from django import forms
from .forms import *

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    raw_id_fields = ('contributors',)
    list_display = ('title', 'category', 'publish_date', '_id')
    search_fields = ('title', 'content')

    def get_object(self, request, object_id, from_field=None):
        try:
            return self.model.objects.get(_id=ObjectId(object_id))
        except (self.model.DoesNotExist, ValueError, TypeError):
            return None

    def delete_model(self, request, obj):
        if obj:
            obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', '_id')
    search_fields = ('name', 'email')

    def get_object(self, request, object_id, from_field=None):
        try:
            return self.model.objects.get(_id=ObjectId(object_id))
        except (self.model.DoesNotExist, ValueError, TypeError):
            return None

    def delete_model(self, request, obj):
        if obj:
            obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


# Register your models here.
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Contributor)
