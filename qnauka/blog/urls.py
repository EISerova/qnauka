from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from blog import views

urlpatterns = [
    path("", views.frontpage, name="frontpage"),
    path("search/", views.search, name="search"),
    re_path(r"^tag/(?P<tag_name>[\w-]+)/$", views.tag_page, name="tag_page"),
    path("<slug:category_slug>/<slug:slug>/", views.detail, name="post_detail"),
    path("<slug:slug>/", views.category, name="category_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
