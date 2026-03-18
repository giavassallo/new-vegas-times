from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class CustomUser(AbstractUser):
    """
    Custom user model that assigns a role per user
    """

    ROLE_READER = "reader"
    ROLE_EDITOR = "editor"
    ROLE_JOUNALIST = "journalist"

    ROLE_CHOICES = [
        (ROLE_READER, "Reader"),
        (ROLE_EDITOR, "Editor"),
        (ROLE_JOUNALIST, "Journalist"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_READER,
    )

    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        related_name="subscribers",
        blank=True,
    )

    subscribed_journalists = models.ManyToManyField(
        "self",
        related_name="jornalists_subscribers",
        symmetrical=False,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        group_name = self.role.capitalize()
        group = Group.objects.filter(name=group_name).first()

        if group:
            self.groups.add(group)

    def __str__(self):
        return self.username 
    

class Publisher(models.Model):
    """
    Represents a publishing organization
    """

    name = models.CharField(max_length=255)

    editors = models.ManyToManyField(
        "CustomUser",
        related_name="publisher_editors",
        blank=True
    )

    journalist = models.ManyToManyField(
        "CustomUser",
        related_name="publisher_journalists",
        blank=True
    )

    def __str__(self):
        return self.name
    

class Article(models.Model):
    """
    Represents a news article
    """

    title = models.CharField(max_length=255)

    content = models.TextField()

    author = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="articles",
    )

    publisher = models.ForeignKey(
        "Publisher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Newsletter(models.Model):
    """
    Collection of articles written by jounalists
    """

    title = models.CharField(max_length=255)

    description = models.TextField()

    author = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="newsletters",
    )

    articles = models.ManyToManyField(
        "Article",
        related_name="newsletters",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

