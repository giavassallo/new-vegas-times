import requests
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article

@receiver(post_save, sender=Article)
def article_approved_signal(sender, instance, created, **kwargs):
    """
    Trigger actions when article is approved
    """

    
    if os.environ.get("RUNNING_TESTS") == "1":
        return

    if instance.approved:
        try:
            requests.post(
                "http://127.0.0.1:8000/api/approved/",
                json={
                    "title": instance.title,
                    "content": instance.content,
                    "author": instance.author.username,
                },
                timeout=5,
            )
            print("Approved article sent to API")
        except requests.exceptions.RequestException:
            print("Could not send approved article to API")