# Generated by Django 2.2.7 on 2020-02-10 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0024_auto_20200210_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='custom_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
