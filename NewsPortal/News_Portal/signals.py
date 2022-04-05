from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


#@receiver(post_save, sender=Post)
def newpost_signal(sender, instance, created, **kwargs):
    post = instance
    categories = post.categories.all()
    recipients = set()

    if not created:
        return

    for category in categories:
        for subscriber in category.subscribers.all():
            recipients.add(subscriber.email)

            html_content = render_to_string(
                'new_post_in_category.html',
                {
                    'user': subscriber,
                    'post': post
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{post.heading}',
                body=post.text[50:],
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subscriber.email
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()