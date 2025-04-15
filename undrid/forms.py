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
            if value == ['on']:
                return []

            valid_values = []
            for val in value:
                try:
                    # Convert string ID to ObjectId
                    obj_id = ObjectId(val)
                    # Query using _id instead of id
                    self.queryset.filter(_id=obj_id).get()
                    valid_values.append(obj_id)  # Store as ObjectId
                except Exception as e:
                    print(f"Invalid ID {val}: {str(e)}")
                    # Skip invalid IDs
                    pass
            return super().clean(valid_values)
        return super().clean(value)

class ArticleForm(forms.ModelForm):
    contributors = MongoDBMultipleChoiceField(
        queryset=Contributor.objects.all(),  # Or your custom contributor queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Article
        fields = ['title', 'category', 'content', 'cover_photo', 'contributors', 'department']
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