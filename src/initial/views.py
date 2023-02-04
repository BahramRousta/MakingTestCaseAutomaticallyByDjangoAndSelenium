from collections import OrderedDict
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DriverSerializer, TestCaseSerializer, TestScenarioSerializer
from .utils import SetUpMain
from .models import Driver, TestScenario, TestStep


class AddDriverAPIView(APIView):

    serializer_class = DriverSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):

            data = serializer.validated_data

            Driver.objects.create(**data)

            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class TestScenarioAPIView(APIView):

    serializer_class = TestScenarioSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetAllTestScenarioAPIView(ListAPIView):
    queryset = TestScenario.objects.all()
    serializer_class = TestScenarioSerializer


class RunTestCaseAPIView(APIView):
    serializer_class = TestCaseSerializer
    set_up = SetUpMain()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            data = serializer.initial_data
            for index in data['test_steps']:

                resultDictionary = OrderedDict((x, y) for x, y in index['action'].items())

                self.set_up.main(**resultDictionary)
            return Response(status=200)
        else:
            return Response(status=400, data=serializer.errors)



