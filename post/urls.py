from django.urls import path
from . import views


app_name = 'post'


urlpatterns = [
    path('', view=views.index, name='index'),
    path('post/<slug>', view=views.index, name='index'),
]
