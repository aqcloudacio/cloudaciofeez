# Generated by Django 2.2.7 on 2020-04-22 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0037_platform_cloned'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='clone_link',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
