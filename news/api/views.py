from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from news.models import Article
from .serializers import ArticleSerializer
from .permissions import IsJournalist, IsEditor
from rest_framework.permissions import IsAuthenticated 


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/articles/  -> list approved articles
    POST /api/articles/  -> create article (journalists only)
    """

    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsJournalist()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/articles/<id>/
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


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

        articles = (
            Article.objects.filter(publisher__in=publishers) |
            Article.objects.filter(author__in=journalists)
        ).filter(approved=True).distinct()

        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data)