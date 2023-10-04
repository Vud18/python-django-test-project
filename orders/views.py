from django.forms import forms
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from customers.models import Customer
from orders.models import Order
from robots.database_queries import sending_mail


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View, forms.Form):

    def post(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)
        post_body = json.loads(request.body)

        robot_serial = post_body.get('robot_serial')
        if len(robot_serial) > 5:
            raise forms.ValidationError(
                'Версия робота введена некорректно',
                params={'robot_serial': post_body.get('robot_serial')},
            )

        book_data = {
            'customer': customer,
            'robot_serial': robot_serial,
        }

        robot_data = Order.objects.create(**book_data)
        data = {
            'message': f'Заказ на робота размещён. Ваш заказ {robot_data.robot_serial}'
        }
        print(f"Функция выполнилась {sending_mail()}")
        return JsonResponse(data, status=201)
