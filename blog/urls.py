from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', view=views.Index.as_view(), name='index'),
    path('<string>', view=views.ListPerCategory.as_view(),
         name='list_per_category'),
    path('login/', view=views.Login.as_view(), name='login'),
    path('logout/', view=views.Logout.as_view(), name='logout'),
    path('register/', view=views.Register.as_view(), name='register'),
    path('post_details/<slug>', view=views.PostDetails.as_view(), name='post_details'),
    path('write_post/', view=views.WritePost.as_view(), name='write_post'),
    path('like_post/<pk>/<like_bool>', view=views.like_post, name='like_post'),
    path('dislike_post/<pk>/<like_bool>',
         view=views.dislike_post, name='dislike_post'),
    path('categories/', view=views.ManageCategories.as_view(), name='categories'),
    path('remove_category/<pk>', view=views.remove_gategory, name='remove_category'),
]
