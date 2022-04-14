from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


@cache_page(20, key_prefix="index_page")
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.POST_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "index": True
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, settings.POST_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "page_obj": page_obj,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    following = request.user.is_authenticated and (
        request.user.follower.filter(author=author).exists()
    )
    paginator = Paginator(post_list, settings.POST_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "author": author,
        "page_obj": page_obj,
        "post_count": post_list.count(),
        "following": following,
    }
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    post_count = author.posts.count()
    form = CommentForm()
    comments = post.comments.all()
    context = {
        "post": post,
        "post_count": post_count,
        "form": form,
        "comments": comments,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    context = {
        "title": "Новый пост",
        "button": "Сохранить",
    }
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect("posts:profile", request.user)
    context["form"] = form
    return render(request, "posts/create.html", context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect("posts:post_detail", post_id)
    context = {
        "title": "Редактировать запись",
        "button": "Добавить",
        "post": post,
    }
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post.id)
    context["form"] = form
    return render(request, "posts/create.html", context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, settings.POST_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "follow": True
    }
    return render(request, "posts/follow.html", context)


@login_required
def profile_follow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    if follower != following:
        Follow.objects.get_or_create(user=follower, author=following)
    return redirect("posts:profile", username=username)


@login_required
def profile_unfollow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    follower.follower.filter(author=following).delete()
    return redirect("posts:profile", username=username)
