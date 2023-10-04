from django.urls import path

from orders.views import OrderView

urlpatterns = [
    path('order/', OrderView.as_view()),
    path('order/<int:customer_id>/', OrderView.as_view()),
    ]
