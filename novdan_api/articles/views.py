from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Article, Medium
from .serializers import ArticleSerializer, MediumSerializer


class Pagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50


class ArticlesView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Article.objects.all().order_by("-published_at")
    serializer_class = ArticleSerializer
    pagination_class = Pagination


class LatestArticlesForMedia(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Article.objects.all().order_by("-published_at")
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        Serializer = self.get_serializer_class()
        media = Medium.objects.all().order_by("id")
        articles = []

        for medium in media:
            medium_serializer = MediumSerializer(medium)
            medium_articles = self.get_queryset().filter(medium=medium)[:10]
            articles_serializer = Serializer(medium_articles, many=True)
            articles.append(
                {
                    **medium_serializer.data,
                    "articles": articles_serializer.data,
                }
            )

        return Response(
            {
                "media": articles,
            }
        )
