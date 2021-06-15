from . import forms
from django.shortcuts import redirect, render
from . import models
from django.views.generic.detail import DetailView
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class Index(ListView):
    model = models.Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return models.Post.objects.filter(is_published=True).order_by('published_date')


class Login(View):
    template_name = 'post/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            return redirect('post:login')

        user = authenticate(self.request, username=username, password=password)

        if not user:
            return redirect('post:login')

        print('\nFazendo login\n')
        login(self.request, user)

        return redirect('post:index')


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)

        return redirect('post:index')


class Register(View):
    template_name = 'post/register.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        context = {
            'register_form': forms.SignUpForm(data=self.request.POST or None),
        }

        self.register_form = context['register_form']

        self.render_template = render(
            self.request, self.template_name, context)

    def get(self, *args, **kwargs):
        print('\nteste \n')
        if self.request.user.is_authenticated:
            return redirect('post:index')

        return self.render_template

    def post(self, *args, **kwargs):
        if not self.register_form.is_valid():
            return self.render_template

        user = User(
            username=self.register_form.cleaned_data.get('username'),
        )

        user.set_password(self.register_form.cleaned_data.get('password'))

        user.save()
        login(self.request, user)

        return redirect('post:index')


class PostDetils(DetailView):
    model = models.Post
    template_name = 'post/post_details.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'


def approve_post(request):
    pass
