from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from . import forms, models


class Index(ListView):
    model = models.Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return models.Post.objects.filter(is_published=True).order_by('published_date')


class ListPerCategory(ListView):
    template_name = 'blog/index.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        category = get_object_or_404(models.Category, name=self.kwargs.get('string'))
        posts = models.Post.objects.filter(categories=category).order_by('published_date')

        self.context = {
            'posts': posts
        }

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.context)


class PostDetails(View):
    template_name = 'blog/post_details.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.post_object = get_object_or_404(
            models.Post, slug=self.kwargs.get('slug'))

        comments = models.Comment.objects.filter(post=self.post_object)

        user_approval = None
        positive_approvals = None
        negative_approvals = None

        if self.request.user.is_authenticated:
            user_approval = models.Aproval.objects.filter(
                user=self.request.user, post=self.post_object).first()

        approvals = models.Aproval.objects.filter(post=self.post_object)

        if approvals:
            positive_approvals = (
                len(approvals.filter(is_approved=True)) / len(approvals)) * 100
            negative_approvals = (
                len(approvals.filter(is_approved=False)) / len(approvals)) * 100

        context = {
            'post': self.post_object,
            'comment_form': forms.CommentForm(self.request.POST or None),
            'comments': comments,
            'user_approval': user_approval,
            'positive_approvals': positive_approvals,
            'negative_approvals': negative_approvals,
        }

        self.comment_form = context['comment_form']

        self.render_template = render(
            self.request, self.template_name, context)

    def get(self, *args, **kwargs):
        return self.render_template

    def post(self, *args, **kwargs):
        if not self.comment_form.is_valid():
            return self.render_template

        comment = models.Comment(
            comment=self.comment_form.cleaned_data.get('comment'),
            author=self.request.user,
            post=self.post_object,
        )

        comment.save()

        return redirect('blog:post_details', slug=self.post_object.slug)


class WritePost(LoginRequiredMixin, View):
    template_name = 'blog/write_post.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        context = {
            'write_post_form': forms.WritePostForm(self.request.POST or None, self.request.FILES or None)
        }

        self.post_form = context['write_post_form']

        self.render_template = render(
            self.request, self.template_name, context)

    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('blog:index')

        return self.render_template

    def post(self, *args, **kwargs):
        if not self.post_form.is_valid():
            return redirect('blog:write_post')

        post = self.post_form.save(commit=False)
        post.author = self.request.user

        post.save()

        messages.success(self.request, 'Post created successfully.')
        return redirect('blog:write_post')


@login_required
def like_post(request, pk, like_bool):
    post = get_object_or_404(models.Post, pk=pk)
    post_approval = models.Aproval.objects.filter(
        post=post, user=request.user).first()

    if not post_approval:
        models.Aproval(
            is_approved=like_bool,
            user=request.user,
            post=post
        ).save()
    else:
        if not post_approval.is_approved:
            post_approval.is_approved = like_bool
            post_approval.save()
        else:
            post_approval.delete()

    return redirect('blog:post_details', slug=post.slug)


@login_required
def dislike_post(request, pk, like_bool):
    post = get_object_or_404(models.Post, pk=pk)
    post_approval = models.Aproval.objects.filter(
        post=post, user=request.user).first()

    if not post_approval:
        models.Aproval(
            is_approved=like_bool,
            user=request.user,
            post=post
        ).save()
    else:
        if not post_approval.is_approved:
            post_approval.delete()
        else:
            post_approval.is_approved = like_bool
            post_approval.save()

    return redirect('blog:post_details', slug=post.slug)


class ManageCategories(LoginRequiredMixin, View):
    template_name = 'blog/categories.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        context = {
            'category_form': forms.CategoryForm(self.request.POST or None),
            'categories': models.Category.objects.all().order_by('name')
        }

        self.category_form = context['category_form']
        self.render_template = render(self.request, self.template_name, context)

    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise Http404()

        return self.render_template

    def post(self, *args, **kwargs):
        if not self.category_form.is_valid():
            return self.render_template

        self.category_form.save()
        
        messages.success(self.request, 'Category added successfully.')
        return redirect('blog:categories')


@login_required
def remove_category(request, pk):
    category = models.Category.objects.get(pk=pk)

    try:
        category.delete()
    except:
        messages.error(
            request,
            f'Not is possible remove the category "{category.name}", as there are posts registered using it.',
        )

    return redirect('blog:categories')


def get_categories(request):
    return {'categories': models.Category.objects.all()}


@login_required(login_url='/accounts/login/')
def edit_category(request, pk):
    if not request.user.is_staff:
        raise Http404()

    categoryName = request.POST.get('name')
    if not categoryName:
        messages.error(request, 'Category name must not be empty.')
    else: 
        category = get_object_or_404(models.Category, pk=pk)

        category.name = categoryName
        category.save()

        messages.success(request, 'Category edited successfully.')

    return redirect('blog:categories')

@login_required
def remove_comment(request, pk):
    comment = models.Comment.objects.get(pk=pk)
    comment.delete()

    return redirect(request.META.get('HTTP_REFERER'))
