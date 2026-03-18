from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


from .views import (
    ArticleListCreateAPIView,
    ArticleDetailAPIView,
    ArticleUpdateAPIView,
    ArticleDeleteAPIView,
    SubscribedArticlesAPIView,
    
)


urlpatterns = [

    path("api/token/", obtain_auth_token),

    path("api/articles/", ArticleListCreateAPIView.as_view()),

    path("api/articles/<int:pk>/", ArticleDetailAPIView.as_view()),

    path("api/articles/<int:pk>/update/", ArticleUpdateAPIView.as_view()),

    path("api/articles/<int:pk>/delete/", ArticleDeleteAPIView.as_view()),

    path("api/articles/subscribed/", SubscribedArticlesAPIView.as_view()),
]