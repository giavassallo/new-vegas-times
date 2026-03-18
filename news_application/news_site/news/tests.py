from django.urls import reverse
from rest_framework.test import APITestCase
import os
from news.models import Article, CustomUser


os.environ["RUNNING_TESTS"] = "1"


class ArticleAPITest(APITestCase):

    def setUp(self):

        self.journalist = CustomUser.objects.create_user(
            username="journalist",
            password="pass",
            role="journalist",
        )

        self.reader = CustomUser.objects.create_user(
            username="reader",
            password="pass",
            role="reader",
        )

        self.article = Article.objects.create(
            title="Test Article",
            content="Content",
            author=self.journalist,
            approved=True,
        )

    def test_reader_can_view_articles(self):

        self.client.login(username="reader", password="pass")

        response = self.client.get("/api/articles/")

        self.assertEqual(response.status_code, 200)

    def test_journalist_can_create_article(self):

        self.client.login(username="journalist", password="pass")

        data = {
            "title": "New Article",
            "content": "Example",
        }

        response = self.client.post("/api/articles/create/", data)

        self.assertEqual(response.status_code, 201)