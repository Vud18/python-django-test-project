import os
from datetime import datetime

from django.conf import settings
from django.forms import forms
from django.http import JsonResponse, HttpResponse
import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .database_queries import sending_mail
from .models import Robot
from .to_exel import convert_to_excel


@method_decorator(csrf_exempt, name='dispatch')
class RobotView(View, forms.Form):

    def post(self, request):
        post_body = json.loads(request.body)
        robot_model = post_body.get('model')
        if len(robot_model) > 2 or len(robot_model) < 1:
            raise forms.ValidationError(
                'Длинна названия модели, введены некорректно!',
                params={'model': post_body.get('model')},
            )

        robot_version = post_body.get('version')
        if len(robot_version) < 1 or len(robot_version) > 2:
            raise forms.ValidationError(
                'Версия робота введена некорректно',
                params={'version': post_body.get('version')},
            )

        robot_created = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        robot_data = {
            'model': robot_model,
            'version': robot_version,
            'serial': f'{robot_model}-{robot_version}',
            'created': robot_created,
        }

        book_obj = Robot.objects.create(**robot_data)
        data = {
            'message': f'Робот модели: {book_obj.id} был добавлен'
        }
        print(f"Функция выполнилась {sending_mail()}")
        return JsonResponse(data, status=201)


def download_file(request):
    convert_to_excel()
    file_path = os.path.join(settings.MEDIA_ROOT, 'D:\\Python Projects\\R4C\\robots\\excel\\teams2.xlsx')

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file_path)

            return response

    return HttpResponse("Файл не найден", status=404)
