# Generated by Django 2.2.7 on 2020-09-21 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0049_auto_20200921_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9),
        ),
    ]