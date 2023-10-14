from django.urls import path

from . import api

urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('read/<uuid:id>/', api.read_notification, name='read_notification'),
    path('readall/', api.read_all_notifications, name='read_all_notifications'),
]
