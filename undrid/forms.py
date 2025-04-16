from django import forms
from .models import *
from django.contrib.auth.models import User


class SearchableMultipleSelect(forms.SelectMultiple):
    class Media:
        js = ('js/searchable_select.js',)  # Create this JS file
        css = {
            'all': ('css/searchable_select.css',)  # Create this CSS file
        }


class MongoDBMultipleChoiceField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        if value:
            object_ids = []
            for val in value:
                try:
                    obj_id = ObjectId(val)
                    self.queryset.get(_id=obj_id)
                    object_ids.append(obj_id)
                except Exception as e:
                    print(f"Invalid contributor ID: {val} — {e}")
            return super().clean(object_ids)
        return super().clean(value)


class MongoDBChoiceField(forms.ModelChoiceField):
    def clean(self, value):
        if value:
            try:
                obj_id = ObjectId(value)
                self.queryset.get(_id=obj_id)
                return super().clean(obj_id)
            except Exception as e:
                print(f"Invalid contributor ID: {value} — {e}")
                raise forms.ValidationError("Invalid contributor selected.")
        return super().clean(value)


class ArticleAdminForm(forms.ModelForm):
    contributors = MongoDBMultipleChoiceField(
        queryset=Contributor.objects.all(),
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Article
        fields = '__all__'


class ArticleForm(forms.ModelForm):
    contributors = MongoDBMultipleChoiceField(
        queryset=Contributor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    researcher = MongoDBChoiceField(
        queryset=Contributor.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Article
        fields = ['title', 'category', 'content', 'cover_photo', 'researcher', 'contributors', 'department']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'cover_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all().order_by('title')


class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['name', 'email', 'bio', 'profile_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }