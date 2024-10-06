from django.contrib import admin
from django.http import HttpResponseRedirect
from django.conf import settings

from unfold.admin import ModelAdmin

from .models import Post, Category, PostComment, Ip

from blog.telegram_utils import send_message_to_telegram, CHAT_ID


from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models

from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget


class CommentItemInLine(admin.TabularInline):
    model = PostComment
    raw_id_fields = ["post"]


@admin.register(Post)
class PostAdmin(ModelAdmin):

    search_fields = ["title", "intro", "body"]
    list_display = [
        "title",
        "slug",
        "category",
        "created_at",
        "status",
        "main_status",
        "total_views",
    ]
    list_filter = ["category", "created_at"]
    prepopulated_fields = {"slug": ("title",)}
    actions_submit_line = ["tg"]

    @admin.action(description="tg")
    def tg(self, request, post_obj):
        """Кнопка для отправки поста в telegram."""

        if request.POST["publish_in_telegram"] == "Publish":
            send_message_to_telegram(chat_id=CHAT_ID, post=post_obj)
            post_obj.is_published = True
            post_obj.save()
            self.message_user(request, "Новость отправлена в Telegram-канал")
            return HttpResponseRedirect(request.path_info)

        return super().tg(request, post_obj)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "slug"]
    list_filter = ["posts"]
    prepopulated_fields = {"slug": ("title",)}

@admin.register(PostComment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["post", "name", "email", "body", "created_at"]
    list_filter = ["post", "name", "email", "created_at"]

@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ["ip"]
