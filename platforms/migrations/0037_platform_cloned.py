# Generated by Django 2.2.7 on 2020-04-22 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0036_remove_platform_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='cloned',
            field=models.BooleanField(default=False),
        ),
    ]
