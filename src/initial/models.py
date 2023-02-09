from django.db import models


class Driver(models.Model):
    """
    WebDriver Model.
    """

    name = models.CharField(max_length=25)
    path = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class TestScenario(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return self.name


class TestCase(models.Model):
    title = models.CharField(max_length=250)
    test_scenario = models.ForeignKey(
        TestScenario,
        on_delete=models.CASCADE,
        related_name='test_cases'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TestStep(models.Model):
    name = models.CharField(max_length=250)
    step = models.JSONField()
    row_number = models.PositiveBigIntegerField()
    test_case = models.ForeignKey(
        TestCase,
        on_delete=models.CASCADE,
        related_name='test_steps'
    )

    def __str__(self):
        return self.name


# class Action(models.Model):
#     class ChoiceAction(models.TextChoices):
#         OPEN_BROWSER = 'open_browser'
#         CLICK = 'click'
#         MOVE_TO_ELEMENT = 'move_to_element'
#         FIND_ELEMENT = 'find_element'
#         SEND_KEYS = 'send_keys'
#         CLOSE = 'close'
#         BACK = 'back'
#         REFRESH = 'refresh'
#
#     name = models.CharField(max_length=25, choices=ChoiceAction.choices)
#
#     def __str__(self):
#         return self.name
