# Generated by Django 2.2.7 on 2020-02-07 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0018_auto_20200207_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='investment',
            name='investment_fee',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=7),
        ),
    ]
