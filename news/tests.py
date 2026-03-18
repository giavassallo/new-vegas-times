from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import CustomUser, Article


class BaseTestCase(TestCase):

    def setUp(self):
        # Create users
        self.reader = CustomUser.objects.create_user(
            username="reader", password="pass", role="reader"
        )
        self.journalist = CustomUser.objects.create_user(
            username="journalist", password="pass", role="journalist"
        )
        self.editor = CustomUser.objects.create_user(
            username="editor", password="pass", role="editor"
        )

        # Create article
        self.article = Article.objects.create(
            title="Test Article",
            content="Content",
            author=self.journalist,
            approved=False
        )


# testing user type permissions
class PermissionTests(BaseTestCase):

    def test_reader_cannot_create_article(self):
        self.client.login(username="reader", password="pass")

        response = self.client.post(reverse("create_article"), {
            "title": "New",
            "content": "Test"
        })

        self.assertEqual(response.status_code, 403)

    def test_journalist_can_create_article(self):
        self.client.login(username="journalist", password="pass")

        response = self.client.post(reverse("create_article"), {
            "title": "New",
            "content": "Test"
        })

        self.assertEqual(response.status_code, 302)

    def test_editor_can_access_dashboard(self):
        self.client.login(username="editor", password="pass")

        response = self.client.get(reverse("editor_dashboard"))
        self.assertEqual(response.status_code, 200)


# testing article lists/details
class ArticleTests(BaseTestCase):

    def test_article_list_view(self):
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)

    def test_article_detail_view(self):
        response = self.client.get(reverse("article_detail", args=[self.article.id]))
        self.assertEqual(response.status_code, 200)


# testing subscriptions
class SubscriptionTests(BaseTestCase):

    def test_subscribe_journalist(self):
        self.client.login(username="reader", password="pass")

        self.client.get(reverse("subscribe_journalist", args=[self.journalist.id]))

        self.assertIn(self.journalist, self.reader.subscribed_journalists.all())

    def test_unsubscribe_journalist(self):
        self.reader.subscribed_journalists.add(self.journalist)

        self.client.login(username="reader", password="pass")

        self.client.get(reverse("unsubscribe_journalist", args=[self.journalist.id]))

        self.assertNotIn(self.journalist, self.reader.subscribed_journalists.all())

    def test_my_feed_only_shows_subscribed(self):
        self.reader.subscribed_journalists.add(self.journalist)
        self.article.approved = True
        self.article.save()

        self.client.login(username="reader", password="pass")

        response = self.client.get(reverse("my_feed"))

        self.assertContains(response, self.article.title)


# testing api
class APITests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_api_requires_auth(self):
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, 401)

    def test_journalist_can_create_article_api(self):
        self.client.login(username="journalist", password="pass")

        response = self.client.post("/api/articles/", {
            "title": "API Article",
            "content": "Test"
        })

        self.assertEqual(response.status_code, 201)


class SignalTests(BaseTestCase):

    @patch("news.signals.requests.post")
    def test_signal_triggers_on_approval(self, mock_post):
        self.article.approved = True
        self.article.save()

        mock_post.assert_called()