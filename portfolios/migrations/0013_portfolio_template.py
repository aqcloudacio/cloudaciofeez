# Generated by Django 2.2.7 on 2020-03-04 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0012_auto_20200304_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='template',
            field=models.BooleanField(default=False),
        ),
    ]
