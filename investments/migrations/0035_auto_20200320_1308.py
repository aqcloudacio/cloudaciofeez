# Generated by Django 2.2.7 on 2020-03-20 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0034_auto_20200319_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='investment_fee',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=7, null=True),
        ),
    ]
