# Generated by Django 2.2.7 on 2020-08-18 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0049_auto_20200817_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentscrapesettings',
            name='xpath_aa_root',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='investmentscrapesettings',
            name='xpath_fee_root',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
