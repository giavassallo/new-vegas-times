import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Newsletter


@csrf_exempt
def approved_article_api(request):
    """
    Receives approved articles via POST
    """

    if request.method == "POST":
        data = json.loads(request.body)

        print("Received approved article: ")
        print(data)

        return JsonResponse({"status": "received"})
    
    return JsonResponse({"error": "Invalid request"})


def article_list(request):
    """
    Display approved articles to readers
    """

    articles = Article.objects.filter(approved=True)

    return render(
        request,
        "news/article_list.html",
        {"articles": articles},
    )


def article_detail(request, pk):
    """
    Show full article
    """

    article = get_object_or_404(Article, pk=pk)

    return render(
        request,
        "news/article_detail.html",
        {"article": article},
    )


@login_required
def create_article(request):
    """
    Journalists create new articles
    """

    if request.user.role != "journalist":
        return redirect("/")

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")

        Article.objects.create(
            title=title,
            content=content,
            author=request.user,
        )

        return redirect("/")

    return render(request, "news/article_create.html")


@login_required
def review_articles(request):
    """
    Editors review unapproved articles
    """

    if request.user.role != "editor":
        return redirect("/")

    articles = Article.objects.filter(approved=False)

    return render(
        request,
        "news/review_articles.html",
        {"articles": articles},
    )


@login_required
def approve_article(request, pk):
    """
    Editor approves article
    """

    if request.user.role != "editor":
        return redirect("/")

    article = get_object_or_404(Article, pk=pk)

    article.approved = True
    article.save()

    return redirect("/review/")


def newsletter_list(request):
    """
    Display newsletters
    """

    newsletters = Newsletter.objects.all()

    return render(
        request,
        "news/newsletter_list.html",
        {"newsletters": newsletters},
    )


@login_required
def editor_dashboard(request):
    """
    Editor dashboard
    """

    if request.user.role != "editor":
        return redirect("/")
    
    articles = Article.objects.filter(approved=False)

    return render(
        request,
        "news/editor_dashboard.html",
        {"articles": articles},
    )