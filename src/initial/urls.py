from django.urls import path
from .views import (
    CreateTestCaseAPIView,
    AddDriverAPIView,
    TestScenarioAPIView,
    GetTestScenarioAPIView,
)

urlpatterns = [
    path('add-driver/', AddDriverAPIView.as_view(), name='add-driver'),
    path('create_test_scenario/', TestScenarioAPIView.as_view(), name='create_test_scenario'),
    path('get_test_scenario/', GetTestScenarioAPIView.as_view(), name='get_test_scenario'),
    path('create-test-case/', CreateTestCaseAPIView.as_view(), name='create-test-case'),
    path('get-test-case/<str:test_case>/', CreateTestCaseAPIView.as_view(), name='get-test-case'),
]
