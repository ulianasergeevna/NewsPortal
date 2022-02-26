import logging
import datetime
from collections import defaultdict
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.contrib.auth.models import User
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def my_job():
    users = User.objects.all()
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)

    for user in users:
        data = defaultdict(list)

        for cat in user.subscriptions.all():
            for post in cat.post_set.filter(publication_time__gte=week_ago).all():
                data[cat.name].append(post)

        if not data:
            continue

        msg = EmailMultiAlternatives(
           subject='News Portal Weekly Digest',
           body=str(data),
           from_email=settings.DEFAULT_FROM_EMAIL,
           to=user.email
        )

        html_content = render_to_string(
            'weekly_digest.html',
            {
                'data': data,
            }
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="sun", hour="00", minute="00"
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")