from django.urls import path
from . import views


urlpatterns = [
    path("", views.article_list, name="article_list"),

    path("article/<int:pk>/", views.article_detail, name="article_detail"),

    path("create/", views.create_article, name="create_article"),

    path("publish/", views.create_article, name="publish_article"),

    path("editor/", views.editor_dashboard, name="editor_dashboard"),

    path("review/", views.review_articles, name="review_articles"),

    path(
        "approve/<int:pk>/",
        views.approve_article,
        name="approve_article",
    ),

    path("newsletters/", views.newsletter_list, name="newsletter_list"),

    path(
        "api/approved/",
        views.approved_article_api,
        name="approved_article_api",
    ),
]