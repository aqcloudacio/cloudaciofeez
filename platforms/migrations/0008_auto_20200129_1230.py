# Generated by Django 2.2.7 on 2020-01-29 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0007_auto_20200128_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platformfamilygroups',
            old_name='platformname_id',
            new_name='platformfamilygroup_id',
        ),
    ]
