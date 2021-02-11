# Generated by Django 2.2.7 on 2020-02-21 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0027_auto_20200220_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='shared_admin_fee',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='platformfees',
            name='admin_fee_rebate',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
    ]