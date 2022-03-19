from django import forms
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe

from . import models


class WritePostForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        min_length=15,
        max_length=255,
    )

    thumbnail = forms.ImageField(
        required=False,
    )

    category = forms.ModelChoiceField(
        required=True,
        queryset=models.Category.objects.all().order_by('name')
    )

    text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 15,
            'cols': 20,
        }),
    )

    publish_now = forms.BooleanField()

    class Meta:
        model = models.Post
        fields = ['category', 'thumbnail', 'title', 'text', 'publish_now']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=255,
        widget=Textarea(),
    )

    class Meta:
        model = models.Comment
        fields = ['comment', ]
