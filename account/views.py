from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View

from . import forms, models


class Login(View):
    template_name = 'account/login.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('blog:index')

        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        try:
            user = authenticate(self.request, username=username, password=password)
            login(self.request, user)

            return redirect('blog:index')
        except:
            messages.error(self.request, 'Username or password is incorrect.')
            return redirect('account:login')

        
class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('blog:index')


class Register(View):
    template_name = 'account/register.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        context = {
            'register_form': forms.RegisterForm(data=self.request.POST or None),
        }

        self.register_form = context['register_form']

        self.render_template = render(
            self.request, self.template_name, context)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('blog:index')

        return self.render_template

    def post(self, *args, **kwargs):
        if not self.register_form.is_valid():
            return self.render_template

        user = models.User(
            username=self.register_form.cleaned_data.get('username'),
            email=self.register_form.cleaned_data.get('email'),
        )

        user.set_password(self.register_form.cleaned_data.get('password'))
        user.save()

        messages.success(
            self.request,
            'Account created successfully. You may log in below with the credentials you provided.',
        )

        return redirect('account:login')


class ForgotPassword(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/forgot.html'
    email_template_name = 'account/reset_password_email.html'
    subject_template_name = 'account/reset_password_subject.txt '
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    
    success_url = reverse_lazy('account:login')
