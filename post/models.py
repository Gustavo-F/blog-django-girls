from django.utils.text import slugify
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.conf import settings
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    thumbnail = models.ImageField(
        upload_to='posts_img/%Y/%m/%d', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    category = models.ForeignKey(Category, on_delete=DO_NOTHING)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    post = models.OneToOneField(Post, on_delete=CASCADE)
    comment_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)


class Aproval(models.Model):
    is_approved = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)

    class Meta:
        unique_together = (('user', 'post'),)
