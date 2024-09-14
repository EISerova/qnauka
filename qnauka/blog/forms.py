from django import forms

from .models import PostComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ("name", "email", "body")
        
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'id':"message", 'placeholder':"Текст комментария", 'rows':"8"}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'id':"name", 'placeholder':"Имя"}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id':"email", 'placeholder':"email"}),
        }
