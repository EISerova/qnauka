from django.conf import settings
from django.conf.urls.static import static
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from .sitemaps import CategorySitemap, PostSitemap

from core.views import about, robot_txt

sitemaps = {"category": CategorySitemap, "post": PostSitemap}

urlpatterns = [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
    path("robots.txt", robot_txt, name="robot_txt"),
    path("admin/", admin.site.urls),
    path("about/", about, name="about"),
    path("", include("blog.urls")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
handler404 = "core.views.page_not_found"

# if settings.DEBUG:
#     # import debug_toolbar

#     # urlpatterns = [
#     #     path('__debug__/', include(debug_toolbar.urls)),
#     # ] + urlpatterns

#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
