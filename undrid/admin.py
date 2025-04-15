from django.contrib import admin
from . models import *
from bson.objectid import ObjectId
from django import forms


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

    def clean_contributors(self):
        contributors = self.cleaned_data.get('contributors')
        # We don't need additional validation here as Django admin handles the selection
        return contributors


class ArticleAdmin(admin.ModelAdmin):
    raw_id_fields = ('contributors',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Handle the many-to-many relationship after saving
        if 'contributors' in form.cleaned_data:
            obj.contributors.clear()  # Clear existing relationships
            for contributor in form.cleaned_data['contributors']:
                obj.contributors.add(contributor)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'contributors':
            kwargs['queryset'] = Contributor.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# Register your models here.
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Contributor)
