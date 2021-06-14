from django.urls import path
from . import views


app_name = 'post'


urlpatterns = [
    path('', view=views.Index.as_view(), name='index'),
    path('login/', view=views.login, name='login'),
    path('register/', view=views.register, name='register'),
    path('post_details/<slug>', view=views.PostDetils.as_view(), name='post_details'),
]
