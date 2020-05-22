from django import forms
from .models import Task, Comment, Contact_Message


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


class PermittedUserAddForm(forms.Form):
    username = forms.CharField()
    allow_comment = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = Contact_Message
        fields = (
            'name',
            'email',
            'subject',
            'message',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Name',
                },
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your Email',
                },
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Subject',
                },
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': 'Message',
                },
            )
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for char in name:
            if not char.isalpha():
                raise forms.ValidationError('Error occurred babe.')
        return name
