import random

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect

from taggit.models import Tag

from .models import Post, Category, Ip
from .forms import CommentForm
from qnauka.settings import SHOWING_POSTS

BAN_LIST_IP = ['10.128.0.35',]


def get_popular_posts():
    return Post.objects.filter(main_status=Post.POPULAR)


def frontpage(request):
    
    ip = get_client_ip(request)
    if ip in BAN_LIST_IP:
        return HttpResponseRedirect('././')
    
    popular_posts = get_popular_posts()
    top_post = Post.objects.filter(main_status=Post.TOP)

    paginator_obj = Paginator(
        Post.objects.filter(status=Post.ACTIVE).filter(main_status=Post.NONE),
        SHOWING_POSTS,
    )
    page = request.GET.get("page")
    posts_list = paginator_obj.get_page(page)

    return render(
        request,
        "posts/frontpage.html",
        {
            "posts_list": posts_list,
            "paginator_obj": paginator_obj,
            "popular_posts": popular_posts,
            "top_post": top_post,
        },
    )


def detail(request, category_slug, slug):
    popular_posts = get_popular_posts()
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    comments = post.comments.all()
    tag = get_object_or_404(Tag, post__id=post.id)
    related_posts = list(post.tags.similar_objects())
    
    if len(related_posts) >= 3:
        random_related_posts = random.sample(related_posts, 3)
    else:
        random_related_posts = related_posts        

    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect(post.get_absolute_url())

    else:
        form = CommentForm()

    ip = get_client_ip(request)
    if ip in BAN_LIST_IP:
        return HttpResponseRedirect('././')

    if Ip.objects.filter(ip=ip).exists():
        post.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        post.views.add(Ip.objects.get(ip=ip))

    return render(
        request,
        "posts/detail.html",
        {
            "post": post,
            "popular_posts": popular_posts,
            "form": form,
            "comments": comments,
            "related_posts": random_related_posts,
            "tag": tag,
        },
    )


def category(request, slug):
    """
    Метод для страницы новостей по категориям,
    page_number - номер страницы из запроса
    """
    popular_posts = get_popular_posts()

    category = get_object_or_404(Category, slug=slug)

    paginator_obj = Paginator(category.posts.filter(status=Post.ACTIVE), SHOWING_POSTS)
    page_number = request.GET.get("page")

    try:
        posts_list = paginator_obj.page(page_number)
    except PageNotAnInteger:
        posts_list = paginator_obj.page(1)
    except EmptyPage:
        return redirect("category_detail", slug=slug)

    return render(
        request,
        "posts/category.html",
        {
            "category": category,
            "posts_list": posts_list,
            "paginator_obj": paginator_obj,
            "popular_posts": popular_posts,
        },
    )


def tag_page(request, tag):
    """
    Метод для страницы новостей по тегам,
    tag_name - название тега для заголовка на странице.
    page_number - номер страницы из запроса
    """
    popular_posts = get_popular_posts()

    tag_name = tag.capitalize().replace("-", " ")
    paginator_obj = Paginator(
        Post.objects.filter(tags__slug=tag).distinct(), SHOWING_POSTS
    )
    page_number = request.GET.get("page")

    try:
        posts_list = paginator_obj.page(page_number)
    except PageNotAnInteger:
        posts_list = paginator_obj.page(1)
    except EmptyPage:
        return redirect("tag_page", tag=tag)

    context = {
        "tag": tag,
        "tag_name": tag_name,
        "posts_list": posts_list,
        "paginator_obj": paginator_obj,
        "popular_posts": popular_posts,
    }

    return render(request, "posts/tag_page.html", context)


def search(request):
    popular_posts = get_popular_posts()

    query = request.GET.get("query", "")
    posts = Post.objects.filter(status=Post.ACTIVE).filter(
        Q(title__iregex=query) | Q(intro__iregex=query) | Q(body__iregex=query)
    )

    return render(
        request,
        "posts/search.html",
        {"posts": posts, "query": query, "popular_posts": popular_posts},
    )


def archive(request):
    """
    Метод для страницы с архивом новостей по тегам,
    создается словарь где ключ tag - тег,
    а значение posts - все посты по тегу
    """
    popular_posts = get_popular_posts()

    tags = Tag.objects.all().order_by("name")
    posts_in_tag = {}
    for tag in tags:
        posts = Post.objects.filter(tags=tag).count()
        posts_in_tag[tag] = posts
    context = {
        "posts_in_tag": posts_in_tag,
        "popular_posts": popular_posts,
    }

    return render(request, "posts/archive.html", context)


# Метод для получения айпи
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
        print('#############', ip)
    else:
        ip = request.META.get("REMOTE_ADDR")  # В REMOTE_ADDR значение айпи пользователя
    return ip
