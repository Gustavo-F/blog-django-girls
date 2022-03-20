from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', view=views.Index.as_view(), name='index'),
    path('posts/<slug>', view=views.PostDetails.as_view(), name='post_details'),
    path('posts/write/', view=views.WritePost.as_view(), name='write_post'),
    path('posts/like/<pk>/<like_bool>', view=views.like_post, name='like_post'),
    path('posts/dislike/<pk>/<like_bool>', view=views.dislike_post, name='dislike_post'),
    path('posts/comments/remove/<pk>', view=views.remove_comment, name='remove_comment'),
    
    path('categories/', view=views.ManageCategories.as_view(), name='categories'),
    path('categories/<string>', view=views.ListPerCategory.as_view(), name='list_per_category'),
    path("categories/edit/<int:pk>", view=views.edit_category, name="edit_category"),
    path('categories/remove/<int:pk>', view=views.remove_category, name='remove_category'),
]
