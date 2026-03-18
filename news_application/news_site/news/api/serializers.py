from rest_framework import serializers

from news.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article model
    """

    class Meta:
        model = Article

        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "approved",
            "created_at",
        ]

        read_only_fields = [
            "author",
            "approved",
            "created_at",
        ]