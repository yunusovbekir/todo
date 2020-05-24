from django import forms
from .models import Task, Comment


class TaskForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'cols': '60'
        }
    ))

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'deadline',
        )
        help_texts = {
            'deadline': 'Example: 2021-01-31 23:49:00'
        }


# -----------------------------------------------------------------------------


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_content",)
        widgets = {
            'comment_content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Write your comment...',
                    'rows': '5',
                },
            ),
        }


# -----------------------------------------------------------------------------


class PermittedUserAddForm(forms.Form):
    username = forms.CharField()
    allow_comment = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )
