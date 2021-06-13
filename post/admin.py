from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)


admin.site.register(models.Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'is_published')
    list_display_links = ('id', 'title', 'category', 'author')
    list_editable = ('is_published', )


admin.site.register(models.Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'comment_date', 'is_approved')
    list_display_links = ('id', 'author', 'post', 'comment_date')
    list_editable = ('is_approved', )


admin.site.register(models.Comment, CommentAdmin)


class AprovalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'is_approved')
    list_display_links = ('id', 'user', 'post')


admin.site.register(models.Aproval, AprovalAdmin)
