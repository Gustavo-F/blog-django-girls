from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import ButtonHolder, Column, Row, Submit
from django import forms
from django.forms.widgets import Textarea
from django_summernote.widgets import SummernoteWidget

from . import models


class WritePostForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        min_length=15,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Title'}),
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
        label='Text',
        required=True,
        widget=SummernoteWidget()
    )

    is_published = forms.BooleanField(
        required=False,
        label='Publish Now'
    )

    class Meta:
        model = models.Post
        fields = ['categories', 'thumbnail', 'is_published', 'title', 'text']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=255,
        widget=Textarea(),
    ) 

    class Meta:
        model = models.Comment
        fields = ['comment']
        

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Add Category'
        })
    )

    class Meta:
        model = models.Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-lg-11'),
                Submit('submit', 'Add', css_class='btn btn-primary col-lg-1 h-50')    
            ),
        )

