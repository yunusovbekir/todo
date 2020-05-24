from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Contact_Message


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
            'email': forms.EmailInput(
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
        """
        Name should contain alphabet and whitespace only.
        Otherwise raise validation error.
        """
        name = self.cleaned_data.get('name')
        if any([
            letter for letter in name if not letter.isalpha()
            and not letter.isspace()
        ]):
            raise forms.ValidationError(_(
                'Are you sure you entered your name correctly?'
            ))
        return name

    def clean_subject(self):
        """
        Entered subject should have at least 6 character of length
        """
        subject = self.cleaned_data.get('subject')
        if len(subject) < 6:
            raise forms.ValidationError(_(
                'Please enter at least 6 chars of subject.'
            ))
        return subject
