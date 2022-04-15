from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    thumbnail = models.ImageField(upload_to='posts_img/%Y/%m/%d', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        super().save()
        self.slug = f'{slugify(self.title)}-{str(self.id)}'

        if not self.published_date and self.is_published:
            self.published_date = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.comment


class Aproval(models.Model):
    is_approved = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'post'),)
