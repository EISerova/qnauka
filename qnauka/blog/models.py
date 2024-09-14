from django.db import models
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    """Модель категорий"""

    title = models.CharField(max_length=255, verbose_name="название")
    slug = models.SlugField(unique=True, verbose_name="слаг категории")

    class Meta:
        ordering = ("-title",)
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/" % self.slug
    
class Ip(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Post(models.Model):
    """Модель статей."""

    ACTIVE = "active"
    DRAFT = "draft"
    POPULAR = "popular"
    TOP = "top"
    NONE = "none"

    CHOICES_STATUS = (
        (ACTIVE, "Active"),
        (DRAFT, "Draft"),
    )

    CHOICES_MAIN = ((POPULAR, "Popular"), (TOP, "Top"), (NONE, "None"))

    category = models.ForeignKey(
        Category,
        related_name="posts",
        on_delete=models.CASCADE,
        verbose_name="категория",
    )
    title = models.CharField(max_length=255, verbose_name="название")
    slug = models.SlugField(verbose_name="слаг статьи")
    intro = models.TextField(max_length=800, blank=True, verbose_name="анонс")
    body = CKEditor5Field(config_name='extends', verbose_name="текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    status = models.CharField(
        max_length=10, choices=CHOICES_STATUS, default=ACTIVE, verbose_name="статус"
    )
    main_status = models.CharField(
        max_length=10,
        choices=CHOICES_MAIN,
        default=NONE,
        verbose_name="блок на главной",
    )
    image = models.ImageField(
        upload_to="uploads/", blank=True, null=True, verbose_name="изображение"
    )
    tags = TaggableManager(blank=True, verbose_name="теги")
    source = models.CharField(
        max_length=80, blank=True, null=True, verbose_name="источник"
    )
    views = models.ManyToManyField(Ip, related_name="post_views", blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Статьи"
        verbose_name = "статья"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/" % (self.category.slug, self.slug)
    
    def total_views(self):
        return self.views.count()
    
    total_views.short_description = 'Просмотры'
    
    @property    
    def structured_data(self):
        url = self.get_absolute_url()
        data = {
            '@type': 'NewsArticle',
            'name': self.title,
            'headline': self.title,
            'alternativeHeadline': self.intro,            
            'datePublished': self.created_at.strftime('%d-%m-%Y'),        
            'url': url,
            'articleSection': self.category.slug,
            'mainEntityOfPage': {
                '@type': 'WebPage',
                '@id': url
            },
        }
        if self.image:
            data['image'] = self.image.url

        return data


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # reply_to = models.ForeignKey('self', related_name='replies',null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "Комментарии"
        verbose_name = "комментарий"

    def __str__(self):
        return self.name