
from .models import Post, Comment
from django import forms

# Comment form

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields  = ('author', 'text',)
        