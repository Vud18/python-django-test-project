from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from robots.views import *
from orders.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("robots.urls")),
    path('', include("orders.urls")),
    # path('robot/', RobotView.as_view()),
]
