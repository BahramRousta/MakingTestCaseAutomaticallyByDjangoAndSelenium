from collections import OrderedDict
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DriverSerializer, TestCaseSerializer, TestScenarioSerializer, GetTestCase
from .utils import SetUpMain
from .models import Driver, TestScenario, TestStep, TestCase


class AddDriverAPIView(APIView):
    """
    Adding WebDriver.
    """
    serializer_class = DriverSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

            Driver.objects.create(**data)

            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class TestScenarioAPIView(APIView):
    """
    Adding TestScenario
    """
    serializer_class = TestScenarioSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetTestScenarioAPIView(ListAPIView):
    queryset = TestScenario.objects.all()
    serializer_class = TestScenarioSerializer


class CreateTestCaseAPIView(APIView):
    """
    It receives the test case with all its test steps
    and executes it by Selenium after validation.
    """

    serializer_class = TestCaseSerializer
    set_up = SetUpMain()

    def get(self, request):
        data = request.query_params['test_case']
        test_case = TestCase.objects.get(title=data)
        test_steps = TestStep.objects.filter(test_case=test_case).order_by("row_number")
        serializer = GetTestCase(test_steps, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # send receiving tests steps with user ordering to
            # SetUpMain Class for running TestCase
            data = serializer.initial_data
            for index in data['test_steps']:
                steps_dict = OrderedDict((x, y) for x, y in index['action'].items())
                self.set_up.main(**steps_dict)

            return Response(status=200, data=data)
        else:
            return Response(status=400, data=serializer.errors)
