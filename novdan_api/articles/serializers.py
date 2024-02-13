from urllib.parse import urlsplit

from rest_framework import serializers

from .models import Article, Medium


class MediumSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()

    def get_icon_url(self, obj):
        if obj.favicon:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.favicon.url)
        hostname = urlsplit(obj.url).netloc or "example.com"
        return f"https://icons.duckduckgo.com/ip3/{hostname}.ico"

    class Meta:
        model = Medium
        fields = ("id", "name", "url", "icon_url")


class ArticleSerializer(serializers.ModelSerializer):
    medium = MediumSerializer()

    class Meta:
        model = Article
        fields = (
            "id",
            "medium",
            "title",
            "description",
            "url",
            "image_url",
            "published_at",
        )
