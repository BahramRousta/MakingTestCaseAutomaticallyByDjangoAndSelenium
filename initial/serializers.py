from rest_framework import serializers
from initial.models import Driver, Action, TestStep


class DriverSerializer(serializers.ModelSerializer):
    """
    Serialize Driver model.
    """

    class Meta:
        model = Driver
        fields = "__all__"


class RunSerializerCore(serializers.Serializer):
    """
    Serialize all steps of TestCase.
    """
    DRIVER_NAME = serializers.CharField(required=False)
    PATH = serializers.CharField(required=False)
    XPATH = serializers.CharField(required=False)
    SEND_KEYS = serializers.CharField(required=False)
    CLICK = serializers.CharField(required=False)
    SLEEP = serializers.IntegerField(required=False)


class SendKeysSerializer(serializers.Serializer):

    value = serializers.CharField(max_length=100)


class ActionSerializer(serializers.Serializer):
    open_browser = serializers.CharField(required=False)
    path = serializers.CharField(max_length=250, required=False)
    find_element = serializers.CharField(required=False)
    time_sleep = serializers.IntegerField(required=False)
    send_keys = SendKeysSerializer(required=False)
    name = serializers.CharField(max_length=15, required=False)
    click = serializers.BooleanField(required=False)


class TestStepSerializer(serializers.ModelSerializer):
    action = ActionSerializer()
    driver_name = serializers.CharField(max_length=25, required=False)

    class Meta:
        model = TestStep

        fields = ["name", "driver_name", "action"]


class RunSerializer(serializers.Serializer):
    """
    Serialize TestCase.
    """

    test_step = serializers.ListField(
        child=TestStepSerializer()
    )