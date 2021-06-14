from typing import List
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from django.views.generic.detail import DetailView
from django.views.generic import ListView


class Index(ListView):
    model = models.Post
    template_name = 'post/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return models.Post.objects.filter(is_published=True).order_by('published_date')


def login(request):
    return render(request, 'post/login.html')


def register(request):
    return render(request, 'post/register.html')


class PostDetils(DetailView):
    model = models.Post
    template_name = 'post/post_details.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
