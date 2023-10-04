from django.urls import path

from .views import *

urlpatterns = [
    path('robot/', RobotView.as_view()),
    path('robot/weekly_report.xlsx', download_file, name='download'),
    ]
