from django import forms
from django.forms.widgets import Textarea

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

    categories = forms.ModelMultipleChoiceField(
        required=True,
        queryset=models.Category.objects.all().order_by('name'),
        widget=forms.SelectMultiple(attrs={
            'class': 'selectpicker',
            'multiple': 'true',
            'data-live-search': 'true',
            'title': 'Search a category...',
            'data-style': 'btn-primary'
        }),
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
        fields = ['categories', 'thumbnail', 'title', 'text', 'publish_now']


class CommentForm(forms.ModelForm):
    # TODO: verificar envio de comentaio em branco
    comment = forms.CharField(
        max_length=255,
        widget=Textarea(),
    ) 

    class Meta:
        model = models.Comment
        fields = ['comment', ]
