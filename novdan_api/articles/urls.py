from django.urls import path

from .views import (
    ArticlesAtomFeed,
    ArticlesRssFeed,
    ArticlesView,
    LatestArticlesForMedia,
)

urlpatterns = [
    path("", ArticlesView.as_view()),
    path("feed/rss/", ArticlesRssFeed()),
    path("feed/atom/", ArticlesAtomFeed()),
    path("latest/", LatestArticlesForMedia.as_view()),
]
