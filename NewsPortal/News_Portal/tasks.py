from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from News_Portal.models import Post


@shared_task
def newpost_signal(post_id):
    post = Post.objects.get(pk=post_id)
    categories = post.categories.all()
    recipients = set()

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