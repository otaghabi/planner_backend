# Generated by Django 4.0 on 2021-12-30 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_advisor_student'),
        ('planners', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='advisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.advisor'),
        ),
    ]