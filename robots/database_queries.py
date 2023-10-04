import django
import os

from django.core.mail import send_mail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "R4C.settings")

django.setup()

import robots.models
import orders.models


def sending_mail():
    search_model = orders.models.Order.objects.all()

    for i in search_model:
        result_search = robots.models.Robot.objects.all().filter(serial__contains=f'{i.robot_serial}')
        if result_search:
            for j in result_search:
                message_for_customer = f"Добрый день! Недавно вы интересовались нашим роботом модели {j.model}, версии {j.version}. Этот робот " \
                                       "теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с " \
                                       "нами "

                print(f'Заказ {j.serial} - удалён')
                deleted_order = orders.models.Order.objects.all().filter(robot_serial=j.serial).delete()

                send_mail(
                    'Subject here',
                    f'{message_for_customer}',
                    'Почта с которой будут идти сообщения',
                    ['Почта на которую буду приходить сообщения'],
                    fail_silently=False,
                )
    return
