# Generated by Django 4.1.5 on 2023-01-24 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initial', '0008_delete_element'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teststep',
            name='test_case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='initial.testcase'),
        ),
    ]
