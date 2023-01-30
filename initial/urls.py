from django.urls import path
from .views import RunTestCaseAPIView, AddDriverAPIView, TestScenarioAPIView

urlpatterns = [
    path('add-driver/', AddDriverAPIView.as_view(), name='add-driver'),
    path('create_test_scenario/', TestScenarioAPIView.as_view(), name='create_test_scenario'),
    path('run-test-case/', RunTestCaseAPIView.as_view(), name='run-test-case'),
]
