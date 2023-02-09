from django.urls import path
from .views import (
    RunTestCaseAPIView,
    AddDriverAPIView,
    TestScenarioAPIView,
    GetAllTestScenarioAPIView,
)

urlpatterns = [
    path('add-driver/', AddDriverAPIView.as_view(), name='add-driver'),
    path('create_test_scenario/', TestScenarioAPIView.as_view(), name='create_test_scenario'),
    path('get_test_scenario/', GetAllTestScenarioAPIView.as_view(), name='get_test_scenario'),
    path('run-test-case/', RunTestCaseAPIView.as_view(), name='run-test-case'),
    path('update-test-case/<int:id>/', RunTestCaseAPIView.as_view(), name='update-test-case'),
    path('get-test-case/<int:id>/', RunTestCaseAPIView.as_view(), name='get-test-case'),
]
