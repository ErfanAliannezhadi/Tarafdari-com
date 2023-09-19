from django import forms
from .models import StatusModel, StatusCommentModel


class StatusCreationForm(forms.ModelForm):
    class Meta:
        model = StatusModel
        fields = ['content', 'file', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-100', 'rows': 3, 'placeholder': 'چیزی بنویسید ...'})
        }


class StatusEditForm(forms.ModelForm):
    class Meta:
        model = StatusModel
        fields = ['content', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-100', 'rows': 3})
        }


class StatusCommentForm(forms.ModelForm):
    class Meta:
        model = StatusCommentModel
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-100', 'rows': 2, 'placeholder': 'دیدگاه خود را بیان کنید ...'})
        }
        labels = {
            'content': ''
        }
