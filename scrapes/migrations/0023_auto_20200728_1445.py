# Generated by Django 2.2.7 on 2020-07-28 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0022_auto_20200728_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investmentscrapesettings',
            old_name='xpath_bs_buy_path',
            new_name='xpath_bs_buy_spread_path',
        ),
        migrations.RenameField(
            model_name='investmentscrapesettings',
            old_name='xpath_bs_sell_path',
            new_name='xpath_bs_sell_spread_path',
        ),
    ]
