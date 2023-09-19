from django import forms
from .models import PostCommentModel, PostModel


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostCommentModel
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 150, 'rows': 5, 'placeholder': 'دیدگاه خود را بنویسید ...'})}
        labels = {'content': ''}


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['title', 'file', 'content', 'tags']
