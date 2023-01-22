from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RunSerializer, DriverSerializer
from .utils import SetUpMain
from .models import Driver


class AddDriverAPIView(APIView):

    serializer_class = DriverSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):

            data = serializer.validated_data

            Driver.objects.create(**data)

            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class RunCheckAPIView(APIView):
    serializer_class = RunSerializer
    set_up = SetUpMain()

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            for key, value in data.items():
                for index, sub_value in value.items():
                    if type(sub_value) == list:
                        for i in sub_value:
                            resultDictionary = dict((x, y) for x, y in i['action'].items())
                            self.set_up.main(**resultDictionary)

            return Response(status=200)
        else:
            return Response(status=400, data=serializer.errors)
