from rest_framework import serializers

from .models import Article, Medium


class MediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medium
        fields = ("id", "name", "url")


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
