# Generated by Django 2.2.7 on 2020-07-22 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0004_aaroot'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentscrape',
            name='prerender_js',
            field=models.BooleanField(default=False),
        ),
    ]
