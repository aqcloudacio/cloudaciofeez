# Generated by Django 2.2.7 on 2020-02-20 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0026_auto_20200220_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platformfees',
            old_name='_ORR_levy',
            new_name='ORR_levy',
        ),
    ]