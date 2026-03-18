from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


from .views import (
    ArticleListAPIView,
    ArticleDetailAPIView,
    ArticleCreateAPIView,
    ArticleUpdateAPIView,
    ArticleDeleteAPIView,
    SubscribedArticlesAPIView,
)

urlpatterns = [

    path("api/token/", obtain_auth_token),

    path(
        "articles/",
        ArticleListAPIView.as_view(),
    ),

    path(
        "articles/<int:pk>/",
        ArticleDetailAPIView.as_view(),
    ),

    path(
        "articles/create/",
        ArticleCreateAPIView.as_view(),
    ),

    path(
        "articles/<int:pk>/update/",
        ArticleUpdateAPIView.as_view(),
    ),

    path(
        "articles/<int:pk>/delete/",
        ArticleDeleteAPIView.as_view(),
    ),

    path(
        "articles/subscribed/",
        SubscribedArticlesAPIView.as_view(),
    ),
]