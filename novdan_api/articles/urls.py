from django.urls import path

from .views import (
    ArticlesAtomFeed,
    ArticlesRssFeed,
    ArticlesView,
    LatestArticlesForMedia,
    MediumView,
)

urlpatterns = [
    path("", ArticlesView.as_view()),
    path("medium/<str:slug>/", MediumView.as_view()),
    path("feed/rss/", ArticlesRssFeed()),
    path("feed/atom/", ArticlesAtomFeed()),
    path("latest/", LatestArticlesForMedia.as_view()),
]
