from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from news.models import Article
from .serializers import ArticleSerializer
from .permissions import IsJournalist, IsEditor

from news.models import Article

from .serializers import ArticleSerializer
from .permissions import IsJournalist, IsEditor


class ArticleListAPIView(generics.ListAPIView):
    """
    GET /api/articles/
    Returns all approved articles.
    """

    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]


class ArticleDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/articles/<id>/
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleCreateAPIView(generics.CreateAPIView):
    """
    POST /api/articles/
    Journalist creates article.
    """

    serializer_class = ArticleSerializer
    permission_classes = [IsJournalist]

    def perform_create(self, serializer):

        serializer.save(author=self.request.user)


class ArticleUpdateAPIView(generics.UpdateAPIView):
    """
    PUT /api/articles/<id>/
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsJournalist]


class ArticleDeleteAPIView(generics.DestroyAPIView):
    """
    DELETE /api/articles/<id>/
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsEditor]


class SubscribedArticlesAPIView(APIView):
    """
    Returns articles from subscribed publishers or journalists.
    """

    def get(self, request):

        user = request.user

        publishers = user.subscribed_publishers.all()
        journalists = user.subscribed_journalists.all()

        articles = Article.objects.filter(
            publisher__in=publishers
        ) | Article.objects.filter(
            author__in=journalists
        )

        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data)