from django.urls import path

from .views import ArticlesView, LatestArticlesForMedia

urlpatterns = [
    path("", ArticlesView.as_view()),
    path("latest/", LatestArticlesForMedia.as_view()),
]
