from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Post, Category, Ip
from .forms import CommentForm
from qnauka.settings import SHOWING_POSTS

def frontpage(request):
    popular_posts = Post.objects.filter(main_status=Post.POPULAR)
    top_post = Post.objects.filter(main_status=Post.TOP)
    
    paginator_obj = Paginator(
        Post.objects.filter(status=Post.ACTIVE).filter(main_status=Post.NONE), SHOWING_POSTS
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
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    popular_posts = Post.objects.filter(main_status=Post.POPULAR)
    comments = post.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            
            return redirect(post.get_absolute_url())
            
    else:
        form = CommentForm()
        
    ip = get_client_ip(request)

    if Ip.objects.filter(ip=ip).exists():
        post.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        post.views.add(Ip.objects.get(ip=ip))  

    return render(
        request, "posts/detail.html", {"post": post, "popular_posts": popular_posts, "form": form, "comments": comments}
    )


def category(request, slug):
    popular_posts = Post.objects.filter(main_status=Post.POPULAR)

    category = get_object_or_404(Category, slug=slug)

    paginator_obj = Paginator(category.posts.filter(status=Post.ACTIVE), SHOWING_POSTS)
    page = request.GET.get("page")
    posts_list = paginator_obj.get_page(page)

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


def tag_page(request, tag_name):
    popular_posts = Post.objects.filter(main_status=Post.POPULAR)
        
    paginator_obj = Paginator(Post.objects.filter(tags__slug=tag_name).distinct(), SHOWING_POSTS)
    page_number = request.GET.get("page")
    posts_list = paginator_obj.get_page(page_number)

    context = {
        "tag_name": tag_name,
        "posts_list": posts_list,
        "paginator_obj": paginator_obj,
        "popular_posts": popular_posts,
    }

    return render(request, "posts/tag_page.html", context)


def search(request):
    popular_posts = Post.objects.filter(main_status=Post.POPULAR)

    query = request.GET.get("query", "")
    posts = Post.objects.filter(status=Post.ACTIVE).filter(
        Q(title__iregex=query) | Q(intro__iregex=query) | Q(body__iregex=query)
    )

    return render(
        request,
        "posts/search.html",
        {"posts": posts, "query": query, "popular_posts": popular_posts},
    )

# Метод для получения айпи
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR') # В REMOTE_ADDR значение айпи пользователя
    return ip