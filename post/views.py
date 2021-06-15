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
    template_name = 'post/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return models.Post.objects.filter(is_published=True).order_by('published_date')


class Login(View):
    template_name = 'post/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            return redirect('post:login')

        user = authenticate(self.request, username=username, password=password)

        if not user:
            return redirect('post:login')

        print('\nFazendo login\n')
        login(self.request, user)

        return redirect('post:index')


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)

        return redirect('post:index')


class Register(View):
    template_name = 'post/register.html'

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
            return redirect('post:index')

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

        return redirect('post:index')


class PostDetails(View):
    template_name = 'post/post_details.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.post_object = get_object_or_404(
            models.Post, slug=self.kwargs.get('slug'))

        comments = models.Comment.objects.filter(post=self.post_object)
        user_approval = models.Aproval.objects.filter(
            user=self.request.user, post=self.post_object).first()

        positive_approvals = None
        negative_approvals = None

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
    template_name = 'post/write_post.html'

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
            return redirect('post:index')

        return self.render_template

    def post(self, *args, **kwargs):
        if not self.write_post_form.is_valid():
            return redirect('post:write_post')

        post = models.Post(
            title=self.write_post_form.cleaned_data.get('title'),
            text=self.write_post_form.cleaned_data.get('text'),
            category=self.write_post_form.cleaned_data.get('category'),
            author=self.request.user,
            thumbnail=self.write_post_form.cleaned_data.get('thumbnail'),
            is_published=self.write_post_form.cleaned_data.get('publish_now'),
        )

        post.save()

        return redirect('post:write_post')


@login_required
def like_post(request, pk, like_bool):
    post = get_object_or_404(models.Post, pk=pk)
    post_approval = models.Aproval.objects.filter(
        post=post, user=request.user).first()

    if not post_approval:
        print('\ncriando\n')
        approval = models.Aproval(
            post=post, user=request.user, is_approved=like_bool)
        approval.save()
    else:
        print(f'VALOR DO OBJETO: {post_approval.is_approved}')

        if post_approval.is_approved:
            print('approved')

            if not like_bool:
                print(f'VALOR PASSADO POR PARAMETRO: {like_bool}')
                print('1 updating...')
                post_approval.is_approved = False
                post_approval.save()
            else:
                print('1 deleting...')
                post_approval.delete()
        else:
            print('not approved')

            if not like_bool:
                post_approval.delete()
                print('2 deleting...')
            else:
                print('2 updating...')
                post_approval.is_approved = True
                post_approval.save()

    return redirect('post:post_details', slug=post.slug)
