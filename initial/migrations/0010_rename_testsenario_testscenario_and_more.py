# Generated by Django 4.1.5 on 2023-01-24 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0009_alter_teststep_test_case'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestSenario',
            new_name='TestScenario',
        ),
        migrations.RenameField(
            model_name='testcase',
            old_name='test_senario',
            new_name='test_scenario',
        ),
    ]