# Generated by Django 2.2.7 on 2020-06-01 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20200601_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='generate',
            field=models.BooleanField(default=False),
        ),
    ]
