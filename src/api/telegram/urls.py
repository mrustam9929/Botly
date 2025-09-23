from django.urls import include, path

from api.telegram.wenhook import webhook

urlpatterns = [
    path('<int:pk>/', webhook, name='telegram-webhook'),
]