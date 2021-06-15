from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=30,
    )

    password = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', ]

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        error_msgs = []
