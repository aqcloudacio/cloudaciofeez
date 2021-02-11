# Generated by Django 2.2.7 on 2020-06-11 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0029_auto_20200610_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='change_orientation_if_overflow',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='structure',
            name='landscape_overflow_limit',
            field=models.PositiveSmallIntegerField(default=7),
        ),
        migrations.AddField(
            model_name='structure',
            name='portrait_overflow_limit',
            field=models.PositiveSmallIntegerField(default=4),
        ),
    ]