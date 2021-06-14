from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'post/index.html')


def login(request):
    return render(request, 'post/login.html')


def register(request):
    return render(request, 'post/register.html')


def post_details(request):
    return render(request, 'post/post_details.html')
