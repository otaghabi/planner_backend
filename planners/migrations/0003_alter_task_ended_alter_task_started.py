# Generated by Django 4.0 on 2022-01-27 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planners', '0002_alter_task_advisor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='ended',
            field=models.DateTimeField(blank=True, null=True, verbose_name='end time'),
        ),
        migrations.AlterField(
            model_name='task',
            name='started',
            field=models.DateTimeField(blank=True, null=True, verbose_name='start time'),
        ),
    ]
