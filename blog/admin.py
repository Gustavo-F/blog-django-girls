from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)


admin.site.register(models.Category, CategoryAdmin)


class PostAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'author', 'is_published')
    list_display_links = ('id', 'title', 'author')
    list_editable = ('is_published', )

    filter_horizontal = ('categories', )
    summernote_fields = ('text', )


admin.site.register(models.Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'author', 'post', 'comment_date', 'is_approved')
    list_display_links = ('id', 'comment', 'author', 'post', 'comment_date')
    list_editable = ('is_approved', )


admin.site.register(models.Comment, CommentAdmin)


class AprovalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'is_approved')
    list_display_links = ('id', 'user', 'post')


admin.site.register(models.Aproval, AprovalAdmin)
