# Generated by Django 2.2.7 on 2020-12-08 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0064_remove_platform_pds_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformnames',
            name='direct_pds_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
