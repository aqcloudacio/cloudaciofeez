# Generated by Django 2.2.7 on 2020-07-31 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0026_auto_20200729_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='aa_pdf',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='bs_pdf',
            field=models.BooleanField(default=False),
        ),
    ]