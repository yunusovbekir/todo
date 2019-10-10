from django import forms
from django.forms.widgets import CheckboxInput
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import *

class DateTimeInput(forms.DateTimeInput):
    input_formats = '%m/%d/%Y %H:%M'

class MyForm(forms.ModelForm):

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
            'can_comment':  CheckboxInput()
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["comment_content"]
