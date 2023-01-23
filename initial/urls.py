from django.urls import path
from .views import RunTestCaseAPIView, AddDriverAPIView

urlpatterns = [
    path('add-driver/', AddDriverAPIView.as_view(), name='add-driver'),
    path('run-test-case/', RunTestCaseAPIView.as_view(), name='run-test-case'),
]
