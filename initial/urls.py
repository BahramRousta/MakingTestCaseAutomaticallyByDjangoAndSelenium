from django.urls import path
from .views import RunCheckAPIView, AddDriverAPIView

urlpatterns = [
    path('add-driver/', AddDriverAPIView.as_view(), name='add-driver'),
    path('run/', RunCheckAPIView.as_view(), name='run'),
]
