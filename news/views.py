import json
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Newsletter
from django.urls import reverse 
from .forms import CustomUserCreationForm
from .models import CustomUser


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")  

        user = CustomUser.objects.create_user(
            username=username,
            password=password
        )

        user.role = role 
        user.save()

        return redirect("login")

    return render(request, "news/register.html")


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
    users = CustomUser.objects.filter(role="journalist")

    return render(
        request,
        "news/article_list.html", {
        "articles": articles,
        "users": users,
    })


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

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.user.role != "journalist":
        return HttpResponseForbidden()

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        Article.objects.create(
            title=title,
            content=content,
            author=request.user,
        )

        return redirect("article_list")

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


@login_required
def subscribe_journalist(request, user_id):
    journalist = get_object_or_404(CustomUser, id=user_id, role="journalist")
    request.user.subscribed_journalists.add(journalist)
    return redirect("article_list")


@login_required
def unsubscribe_journalist(request, user_id):
    journalist = get_object_or_404(CustomUser, id=user_id, role="journalist")
    request.user.subscribed_journalists.remove(journalist)
    return redirect("article_list")


@login_required
def my_feed(request):
    journalists = request.user.subscribed_journalists.all()
    articles = Article.objects.filter(author__in=journalists, approved=True)

    return render(request, "news/article_list.html", {"articles": articles})