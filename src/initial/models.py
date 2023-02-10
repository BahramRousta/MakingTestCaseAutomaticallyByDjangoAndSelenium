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
