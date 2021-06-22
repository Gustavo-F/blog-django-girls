from django.contrib import messages
from django.http.response import HttpResponse
from . import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from . import models
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(ListView):
    model = models.Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return models.Post.objects.filter(is_published=True).order_by('published_date')


class Login(View):
    template_name = 'blog/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            return redirect('blog:login')

        user = authenticate(self.request, username=username, password=password)

        if not user:
            return redirect('blog:login')

        print('\nFazendo login\n')
        login(self.request, user)

        return redirect('blog:index')


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)

        return redirect('blog:index')


class Register(View):
    template_name = 'blog/register.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        context = {
            'register_form': forms.SignUpForm(data=self.request.POST or None),
        }

        self.register_form = context['register_form']

        self.render_template = render(
            self.request, self.template_name, context)

    def get(self, *args, **kwargs):
        print('\nteste \n')
        if self.request.user.is_authenticated:
            return redirect('blog:index')

        return self.render_template

    def post(self, *args, **kwargs):
        if not self.register_form.is_valid():
            return self.render_template

        user = User(
            username=self.register_form.cleaned_data.get('username'),
        )

        user.set_password(self.register_form.cleaned_data.get('password'))

        user.save()
        login(self.request, user)

        return redirect('blog:index')


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

        return self.render_template


class WritePost(LoginRequiredMixin, View):
    template_name = 'blog/write_post.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        context = {
            'write_post_form': forms.WritePostForm(self.request.POST or None, self.request.FILES or None)
        }

        self.write_post_form = context['write_post_form']

        self.render_template = render(
            self.request, self.template_name, context)

    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('blog:index')

        return self.render_template

    def post(self, *args, **kwargs):
        if not self.write_post_form.is_valid():
            return redirect('blog:write_post')

        post = models.Post(
            title=self.write_post_form.cleaned_data.get('title'),
            text=self.write_post_form.cleaned_data.get('text'),
            category=self.write_post_form.cleaned_data.get('category'),
            author=self.request.user,
            thumbnail=self.write_post_form.cleaned_data.get('thumbnail'),
            is_published=self.write_post_form.cleaned_data.get('publish_now'),
        )

        post.save()

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


class Categories(LoginRequiredMixin, View):
    template_name = 'blog/categories.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        context = {
            'categories': models.Category.objects.all().order_by('name')
        }

        self.render_template = render(
            self.request, self.template_name, context)

    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('blog:index')

        return self.render_template

    def post(self, *args, **kwargs):
        if models.Category.objects.filter(name=self.request.POST.get('add_category_input')):
            return redirect('blog:categories')

        category = models.Category(
            name=self.request.POST.get('add_category_input'))

        category.save()

        return redirect('blog:categories')


def remove_gategory(request, pk):
    category = models.Category.objects.get(pk=pk)

    try:
        category.delete()
    except:
        messages.error(
            request,
            f'Not is possible remove the category "{category.name}", as there are posts registered using it.',
        )

    return redirect('blog:categories')
