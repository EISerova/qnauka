from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Post

from django.core.paginator import Paginator


def main_posts(request):
    popular_posts = Post.objects.filter(main_status=Post.POPULAR)

    return render(request, "base.html", {"popular_posts": popular_posts})


def about(request):
    popular_posts = Post.objects.filter(main_status=Post.POPULAR)

    return render(request, "about.html", {"popular_posts": popular_posts})


def robot_txt(request):
    text = ["User-Agent: *", "Disallow: /admin/", "Sitemap: /sitemap.xml/"]
    return HttpResponse("\n".join(text), content_type="text/plain")


def page_not_found(request, exception):
    popular_posts = Post.objects.filter(main_status=Post.POPULAR)

    return render(
        request,
        "error_pages/404.html",
        {"path": request.path, "popular_posts": popular_posts},
        status=404,
    )
