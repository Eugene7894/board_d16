import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User


from board_app.models import Post


logger = logging.getLogger(__name__)


def news_sender():
    #  Your job processing logic here...
        url = ''
        week_posts = Post.objects.filter(
            creationDate__range=[timezone.now() - timedelta(hours=24), timezone.now()],
        )

        if week_posts.exists():
            for week_post in week_posts:
                url += f'{week_post.title} http://127.0.0.1:8000{week_post.get_absolute_url()}, \n'

            for user in User.objects.all():
                send_mail(
                    subject=f'Объявления на Board_D16 за сегодня!',
                    message=f'Привет {user.username}, объявления за сегодня: {url}',
                    from_email='projects-mail-sf@yandex.ru',
                    recipient_list=[user.email]
                )


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            news_sender,
            trigger=CronTrigger(hour="22"),
            # отправляем письма подписчикам каждый день в 22.00 hour="22"
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="news_sender",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="09", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
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