# Generated by Django 2.2.7 on 2020-02-21 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0029_auto_20200221_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformfees',
            name='admin_fee_rebate',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=7),
        ),
    ]