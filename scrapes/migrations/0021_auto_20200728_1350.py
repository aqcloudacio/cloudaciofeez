# Generated by Django 2.2.7 on 2020-07-28 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0020_auto_20200728_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='xpath_bs_name_path',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='xpath_bs_path',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
