from django import forms
from .models import Task, Comment


class DateTimeInput(forms.DateTimeInput):
    input_formats = '%m/%d/%Y %H:%M'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        deadline = forms.DateField(
            widget=forms.DateTimeInput(
                attrs={'type': 'date'}
            )
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_content",)
        widgets = {
            'comment_content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment...',
                'rows': '5',
            })
        }


class PermittedUserAddForm(forms.Form):
    username = forms.CharField()
    allow_comment = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )
