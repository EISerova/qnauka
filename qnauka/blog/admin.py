from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Post, Category, PostComment, Ip

class CommentItemInLine(admin.TabularInline):
    model = PostComment
    raw_id_fields = ['post']

class PostAdmin(ModelAdmin):
    
    search_fields = ['title', 'intro', 'body']
    list_display = ['title', 'slug', 'category', 'created_at', 'status', "main_status", 'total_views']
    list_filter = ['category', 'created_at']
    inlines = [CommentItemInLine]
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "slug"]
    list_filter = ["posts"]
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['post', 'name', 'email', 'body', 'created_at']
    list_filter = ['post', 'name', 'email', 'created_at']
    
class IpAdmin(admin.ModelAdmin):
    list_display = ['ip']

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostComment, CommentAdmin)
admin.site.register(Ip, IpAdmin)
