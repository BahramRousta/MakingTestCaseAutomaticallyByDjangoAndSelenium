from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from initial.models import Driver, TestStep, TestCase, TestScenario


class DriverSerializer(serializers.ModelSerializer):
    """
    Serialize WebDriver model.
    """

    class Meta:
        model = Driver
        fields = "__all__"


class SendKeysSerializer(serializers.Serializer):
    """
    Serialize SendKeys value.
    """
    value = serializers.CharField(max_length=100)


class ActionSerializer(serializers.Serializer):
    """
    Serialize Selenium action and Keywords to send from TestCases.
    """

    web_driver = serializers.CharField(required=False)
    path = serializers.CharField(max_length=250, required=False)
    find_element = serializers.CharField(required=False)
    time_sleep = serializers.IntegerField(required=False)
    send_keys = SendKeysSerializer(required=False)
    name = serializers.CharField(max_length=15, required=False)
    click = serializers.BooleanField(required=False)
    close = serializers.BooleanField(required=False)


class TestStepSerializer(serializers.ModelSerializer):
    """
    Serialize TestSteps that senf from TestCase.
    """
    action = ActionSerializer()

    class Meta:
        model = TestStep

        fields = ["row_number", "name", "action"]


class TestScenarioSerializer(serializers.ModelSerializer):
    """
    Serialize TestScenario.
    """
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

    test_scenario = serializers.IntegerField(required=True, write_only=True)
    test_steps = serializers.ListField(
        child=TestStepSerializer()
    )

    class Meta:
        model = TestCase
        fields = ['id', 'test_scenario', 'title', 'test_steps']
        extra_fields = {
            "id": {"required": "False",
                   "read_only": "True"},
            "test_steps": {"read_only": "True",
                           "write_only": "True"}
        }

    def validate(self, attrs):
        """
        If the sent keywords are not serializer fields and Also if the row number and steps name
        has duplicates return ValidationError.
        """

        data = self.initial_data['test_steps']
        for key in data:
            for k, v in key['action'].items():
                if k not in ActionSerializer().fields:
                    raise ValidationError(
                        {'Message': f'In test_step "{key["name"]}",{k} is not a valid keyword.'}
                    )

        for i, element in enumerate(data):
            current_element = element
            next_element = data[i + 1] if i < len(data) - 1 else None

            if next_element is not None:
                if current_element['row_number'] == next_element['row_number']:
                    raise ValidationError(
                        {'Message': 'row number can not be duplicate.'}
                    )

                if current_element['name'] == next_element['name']:
                    raise ValidationError(
                        {'Message': 'name can not be duplicate.'}
                    )

        return attrs

    def validate_test_scenario(self, attr):

        test_scenario_id = attr
        test_scenario = TestScenario.objects.filter(id=test_scenario_id)

        if not test_scenario.exists():
            raise ValidationError({'Message': 'Test scenario in not exist.'})
        return attr

    def create(self, validated_data):
        """
        Create new test case and save test steps.
        """

        test_scenario_id = validated_data['test_scenario']

        test_scenario = TestScenario.objects.filter(id=test_scenario_id).first()

        if test_scenario:
            test_case = TestCase.objects.filter(title=validated_data['title'],
                                                test_scenario=test_scenario)

            if not test_case.first():
                new_test_case = TestCase.objects.create(test_scenario=test_scenario,
                                                        title=validated_data['title'])

                for step in validated_data['test_steps']:
                    TestStep.objects.create(row_number=step['row_number'],
                                            name=step['name'],
                                            step=step['action'],
                                            test_case=new_test_case)
                return new_test_case
            else:
                test_step = None
                for step in validated_data['test_steps']:

                    test_step = TestStep.objects.filter(Q(row_number=step['row_number']) | Q(name=step['name']),
                                                        test_case=test_case.first()).first()

                    if test_step and test_step.row_number == step['row_number']:
                        test_step.name = step['name']
                        test_step.step = step['action']
                        test_step.save()
                    elif test_step and test_step.name == step['name']:
                        test_step.row_number = step['row_number']
                        test_step.step = step['action']
                        test_step.save()
                    else:
                        test_step = TestStep.objects.create(row_number=step['row_number'],
                                                            name=step['name'],
                                                            step=step['action'],
                                                            test_case=test_case.first())
                return test_step

    # def update(self, instance, validated_data):
    #
    #     for step in validated_data['test_steps']:
    #         test_step = TestStep.objects.filter(name=step['name'],
    #                                             row_number=step['row_number'],
    #                                             test_case=instance).first()
    #         if test_step:
    #             test_step.step = step['action']
    #             test_step.save()
    #         else:
    #             TestStep.objects.create(row_number=step['row_number'],
    #                                     name=step['name'],
    #                                     step=step['action'],
    #                                     test_case=instance)
    #     return instance


class GetTestCase(serializers.ModelSerializer):
    class Meta:
        model = TestStep

        fields = ["row_number", "name", "step"]
