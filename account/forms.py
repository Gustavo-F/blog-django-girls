from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import ButtonHolder, Column, Row, Submit
from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=30,
    )

    email = forms.EmailField(
        required=True,
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
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('username')),
            Row(Column('email')),
            Row(Column('password')),
            Row(Column('confirm_password')),
        )
        