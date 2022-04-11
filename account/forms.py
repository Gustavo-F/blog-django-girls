from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import ButtonHolder, Column, Row, Submit
from django import forms
from django.contrib.auth.models import User

from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    email = forms.EmailField(
        label='',
        required=True,
        validators=[EmailValidator],
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    password = forms.CharField(
        label='',
        required=True,
        max_length=30,
        validators=[validate_password],
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    confirm_password = forms.CharField(
        label='',
        required=True,
        max_length=30,
        validators=[validate_password],
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', ]

    def clean(self):
        super().clean()
        data = self.cleaned_data
        validation_msgs = {}

        if data.get('password') != data.get('confirm_password'):
            validation_msgs['password'] = "Passwords didn't match."
            validation_msgs['confirm_password'] = "Passwords didn't match."

        raise forms.ValidationError(validation_msgs)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('username', css_class='mb-3')),
            Row(Column('email', css_class='mb-3')),
            Row(Column('password', css_class='mb-3')),
            Row(Column('confirm_password', css_class='mb-4')),
            ButtonHolder(Submit('submit', 'Register', css_class='w-100')),
        )
        