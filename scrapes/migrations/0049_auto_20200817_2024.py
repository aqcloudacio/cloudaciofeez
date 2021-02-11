# Generated by Django 2.2.7 on 2020-08-17 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0048_investmentscrapesettings_bs_split_name_string'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='fee_slugify_path',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='fee_slugify_path_no_hyphens',
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name='investmentscrape',
            constraint=models.UniqueConstraint(fields=('name', 'settings'), name='unique_investment_scrape'),
        ),
    ]
