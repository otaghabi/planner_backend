# Generated by Django 4.0 on 2022-02-01 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='NONE', max_length=4, verbose_name='Gender'),
        ),
    ]