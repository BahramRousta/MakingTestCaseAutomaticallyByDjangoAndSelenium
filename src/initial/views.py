from collections import OrderedDict
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DriverSerializer, TestCaseSerializer, TestScenarioSerializer, GetTestCase
from .utils import SetUpMain
from .models import Driver, TestScenario, TestStep, TestCase


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

            # data = serializer.initial_data
            # for index in data['test_steps']:
            #
            #     resultDictionary = OrderedDict((x, y) for x, y in index['action'].items())
            #
            #     self.set_up.main(**resultDictionary)
            return Response(status=200)
        else:
            return Response(status=400, data=serializer.errors)

    def put(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            test_scenario_id = data['test_scenario']
            test_scenario = TestScenario.objects.filter(id=test_scenario_id).first()
            if test_scenario:
                test_case = TestCase.objects.filter(title=data['title'],
                                                    test_scenario=test_scenario).first()
                if not test_case:
                    return Response(status=400, data={"Message": f"Test case {data['title']} not exist."})
                serializer.update(instance=test_case, validated_data=data)
            return Response(status=200)
        else:
            return Response(status=400, data=serializer.errors)
