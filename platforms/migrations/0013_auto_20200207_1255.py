# Generated by Django 2.2.7 on 2020-02-07 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0012_auto_20200131_1250'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='platform',
            name='unique_platform_template',
        ),
        migrations.AddConstraint(
            model_name='platform',
            constraint=models.UniqueConstraint(condition=models.Q(template=True), fields=('name',), name='unique_platform_template'),
        ),
    ]
