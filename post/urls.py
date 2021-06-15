from django.urls import path
from . import views


app_name = 'post'


urlpatterns = [
    path('', view=views.Index.as_view(), name='index'),
    path('login/', view=views.Login.as_view(), name='login'),
    path('logout/', view=views.logout, name='logout'),
    path('register/', view=views.Register.as_view(), name='register'),
    path('post_details/<slug>', view=views.PostDetils.as_view(), name='post_details'),
]
