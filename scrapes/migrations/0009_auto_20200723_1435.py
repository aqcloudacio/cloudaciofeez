# Generated by Django 2.2.7 on 2020-07-23 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0008_auto_20200723_1352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investmentscrape',
            old_name='prerender_js',
            new_name='aa_prerender_js',
        ),
        migrations.AddField(
            model_name='investmentscrape',
            name='fee_prerender_js',
            field=models.BooleanField(default=False),
        ),
    ]
