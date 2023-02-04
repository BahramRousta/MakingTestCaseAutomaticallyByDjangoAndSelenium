from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from initial.models import Driver, TestStep, TestCase, TestScenario


class DriverSerializer(serializers.ModelSerializer):
    """
    Serialize Driver model.
    """

    class Meta:
        model = Driver
        fields = "__all__"


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
    close = serializers.BooleanField(required=False)


class TestStepSerializer(serializers.ModelSerializer):
    action = ActionSerializer()

    class Meta:
        model = TestStep

        fields = ["name", "action"]


class TestScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScenario
        fields = ['id', 'name']
        extra_fields = {
            "id": {"required": "False",
                   "read_only": "True"}
        }

class TestCaseSerializer(serializers.ModelSerializer):
    """
    Serialize TestCase.
    """

    test_scenario = serializers.IntegerField(required=True)
    test_steps = serializers.ListField(
        child=TestStepSerializer()
    )

    class Meta:
        model = TestCase
        fields = ['id', 'test_scenario', 'title', 'test_steps']
        extra_fields = {
            "id": {"required": "False",
                   "read_only": "True"}
        }

    def validate(self, attrs):

        for key in self.initial_data['test_steps']:
            for keyword, value in key['action'].items():
                if keyword not in ActionSerializer().fields:
                    raise ValidationError({'Error': f'In test_step "{key["name"]}",'
                                                    f' {keyword} is not a valid keyword.'})

        return attrs

    def validate_test_scenario(self, attr):

        test_scenario_id = attr
        test_scenario = TestScenario.objects.filter(id=test_scenario_id)

        if not test_scenario.exists():
            raise ValidationError({'Error': 'Test scenario in not exist.'})
        return attr

    def create(self, validated_data):
        """
        Create new test case and test steps.
        :param validated_data:
        :return: TestCase Model Instance
        """

        test_scenario_id = validated_data['test_scenario']

        test_scenario = TestScenario.objects.filter(id=test_scenario_id).first()

        if test_scenario:
            # test_case = TestCase.objects.filter(title=validated_data['title'],
            #                                     test_scenario=test_scenario)

            # if not test_case.first():
            new_test_case = TestCase.objects.create(test_scenario=test_scenario,
                                                    title=validated_data['title'])

            for step in validated_data['test_steps']:
                TestStep.objects.create(name=step['name'],
                                        step=step['action'],
                                        test_case=new_test_case)
            return new_test_case
            # raise ValidationError(f"Test case {validated_data['title']} already exists."
            #                       f" To insert it, you will need first to update it.")