from django import forms
from django.forms.widgets import CheckboxInput
from .models import Task, Permitted_Users, Comment


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


class PermittedUsersForm(forms.ModelForm):
    class Meta:
        model = Permitted_Users
        fields = ['permitted_username', 'can_comment']
        widgets = {
            'can_comment': CheckboxInput()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_content"]


class PermittedUserAddForm(forms.Form):
    username = forms.CharField()
