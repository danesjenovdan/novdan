from uuid import uuid4

from django.db import models


def media_favicon_path(instance, filename):
    return f"media_favicon_{instance.id}_{filename}"


class Medium(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=64)
    url = models.URLField()
    favicon = models.ImageField(upload_to=media_favicon_path, null=True, blank=True)
    article_rss_urls = models.TextField(blank=True, null=True)
    image_css_selector = models.CharField(max_length=256, default="article img")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Media"

    def __str__(self):
        return f"{self.name}"


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    medium = models.ForeignKey(
        Medium,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    title = models.CharField(max_length=256, blank=True)
    description = models.TextField(null=True, blank=True)
    guid = models.CharField(max_length=256)
    url = models.URLField(max_length=512)
    image_url = models.URLField(max_length=512, null=True, blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title} ({self.id})"
