# Generated by Django 4.2.15 on 2024-08-21 12:47

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="название")),
                ("slug", models.SlugField(unique=True, verbose_name="слаг категории")),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "Категории",
                "ordering": ("-title",),
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="название")),
                ("slug", models.SlugField(verbose_name="слаг статьи")),
                (
                    "intro",
                    models.TextField(blank=True, max_length=800, verbose_name="анонс"),
                ),
                ("body", models.TextField(blank=True, verbose_name="текст")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата создания"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("draft", "Draft")],
                        default="active",
                        max_length=10,
                        verbose_name="статус",
                    ),
                ),
                (
                    "main_status",
                    models.CharField(
                        choices=[
                            ("popular", "Popular"),
                            ("top", "Top"),
                            ("none", "None"),
                        ],
                        default="none",
                        max_length=10,
                        verbose_name="блок на главной",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="uploads/",
                        verbose_name="изображение",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True, max_length=80, null=True, verbose_name="источник"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to="blog.category",
                        verbose_name="категория",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="теги",
                    ),
                ),
            ],
            options={
                "verbose_name": "статья",
                "verbose_name_plural": "Статьи",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="blog.post",
                    ),
                ),
            ],
        ),
    ]
