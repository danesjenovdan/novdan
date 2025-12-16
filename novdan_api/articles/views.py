from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Article, Medium
from .serializers import ArticleSerializer, MediumMoreSerializer


class Pagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50


class MediumView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MediumMoreSerializer
    lookup_field = "slug"
    queryset = Medium.objects.all()


class ArticlesView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    pagination_class = Pagination

    def get_queryset(self):
        qs = Article.objects.all().order_by("-published_at")

        medium__slug = self.request.query_params.get("medium__slug")
        if medium__slug:
            return qs.filter(medium__slug=medium__slug)

        return qs


class ArticlesRssFeed(Feed):
    feed_type = Rss201rev2Feed
    title = "Nov dan"
    description = "Neposredna podpora neodvisnim medijskim ustvarjalcem"
    link = "https://novdan.si/"
    feed_url = "https://denarnica.novdan.si/articles/feed/rss/"
    language = "sl"

    def items(self):
        return Article.objects.all().order_by("-published_at")[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.url

    def item_pubdate(self, item):
        return item.published_at

    def item_updateddate(self, item):
        return item.updated_at

    def item_author_name(self, item):
        return item.medium.name

    def item_author_link(self, item):
        return item.medium.url

    item_guid_is_permalink = False

    def item_guid(self, item):
        return f"urn:uuid:{item.id}"


class ArticlesAtomFeed(ArticlesRssFeed):
    feed_type = Atom1Feed
    subtitle = ArticlesRssFeed.description
    feed_url = "https://denarnica.novdan.si/articles/feed/atom/"


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
