from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserReply, Post


@receiver(post_save, sender=UserReply)
def send_msg(instance, created, **kwargs):
    """функция-сигнал, которая срабатывает, когда в модель UserReply (отклики) вносятся изменения
    если создается новая запись (if created), то автору объявления отправляется письмо-уведомление,
    если автор объявления принимает отклик, то автору отклика придет письмо"""
    user_author = Post.objects.get(pk=instance.postReply_id).authorUser
    post_tittle = Post.objects.get(pk=instance.postReply_id).title
    reply_text = UserReply.objects.get(pk=instance.id).text

    if created:
        # Если создан новый отклик, то автору письма отправить письмо-уведомлений
        send_mail(
            subject=f'У вас новый отклик на Board_D16!',
            message=f'Здравствуйте, {user_author.username}, на ваше объявление "{post_tittle}" пришел новый отклик:\n'
                    f'"{reply_text}" , подробнее http://127.0.0.1:8000/replies/ .',
            from_email='projects-mail-sf@yandex.ru',
            recipient_list=[user_author.email]
        )

    elif instance.is_accepted:
        # Если отклик принят, то автору отклика отправить письмо-уведомление
        user_reply = User.objects.get(pk=instance.userReply_id)

        send_mail(
            subject=f'Ваш отклик на Board_D16 одобрен!',
            message=f'Здравствуйте, {user_reply.username}, ваше отклик на объявление "{post_tittle}" принят!',
            from_email='projects-mail-sf@yandex.ru',
            recipient_list=[user_reply.email]
        )
