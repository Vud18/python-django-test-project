from datetime import datetime, timedelta

import django
import openpyxl
import os

from django.db.models import Count
from django.utils.timezone import make_aware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "R4C.settings")

django.setup()

import robots.models


def get_data_last_week():
    current_datetime = datetime.now()
    one_week_ago = current_datetime - timedelta(days=7)
    one_week_ago = make_aware(one_week_ago)

    queryset = robots.models.Robot.objects.filter(created__gte=one_week_ago)
    return queryset


def convert_to_excel():
    to_week_queryset = get_data_last_week()
    queryset = to_week_queryset.values('model', 'version').annotate(total_versions=Count('version'))

    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    worksheet['A1'] = 'Модель'
    worksheet['B1'] = 'Версия'
    worksheet['C1'] = 'Количество за неделю'

    for counter, items in enumerate(queryset, start=2):
        worksheet[counter][0].value = items['model']
        worksheet[counter][1].value = items['version']
        worksheet[counter][2].value = items['total_versions']

    workbook.save('D:\\Python Projects\\R4C\\robots\\excel\\teams2.xlsx')
    workbook.close()
