from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
        widgets = {
            'email': forms.EmailInput(),
        }

    def clean_first_name(self):
        """
        Name should contain alphabet and whitespace only.
        Otherwise raise validation error.
        """
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            if any([
                letter for letter in first_name if not letter.isalpha()
                and not letter.isspace()
            ]):
                raise forms.ValidationError(_(
                    'Are you sure you entered your first name correctly?'
                ))
            return first_name

    def clean_last_name(self):
        """
        Name should contain alphabet and whitespace only.
        Otherwise raise validation error.
        """
        last_name = self.cleaned_data.get('last_name')

        if last_name:
            if any([
                letter for letter in last_name if not letter.isalpha()
                and not letter.isspace()
            ]):
                raise forms.ValidationError(_(
                    'Are you sure you entered your first name correctly?'
                ))
            return last_name
