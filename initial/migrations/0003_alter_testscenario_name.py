# Generated by Django 4.1.1 on 2023-01-30 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0002_remove_testcase_test_step_teststep_test_case'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testscenario',
            name='name',
            field=models.CharField(db_index=True, max_length=250, unique=True),
        ),
    ]