from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),

    path("", views.article_list, name="article_list"),

    path("article/<int:pk>/", views.article_detail, name="article_detail"),

    path("create/", views.create_article, name="create_article"),

    # publish page
    path("publish/", views.create_article, name="publish_article"),

    # editor dashboard
    path("editor/", views.editor_dashboard, name="editor_dashboard"),

    # review page
    path("review/", views.review_articles, name="review_articles"),

    #article approval
    path(
        "approve/<int:pk>/",
        views.approve_article,
        name="approve_article",
    ),

    # newsletter list
    path("newsletters/", views.newsletter_list, name="newsletter_list"),

    # subscribe/unsubscribe feature
    path("subscribe/<int:user_id>/", views.subscribe_journalist, name="subscribe_journalist"),
    path("unsubscribe/<int:user_id>/", views.unsubscribe_journalist, name="unsubscribe_journalist"),

    # feed of user subscriptions
    path("my-feed/", views.my_feed, name="my_feed"),

    # api
    path(
        "api/approved/",
        views.approved_article_api,
        name="approved_article_api",
    ),
]