# Generated by Django 2.2.7 on 2020-02-20 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0024_auto_20200220_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platformfees',
            name='ORR_levy_cap',
        ),
        migrations.RemoveField(
            model_name='platformfees',
            name='admin_fee_cutoff',
        ),
        migrations.RemoveField(
            model_name='platformfees',
            name='white_label_admin_fee',
        ),
    ]