# Generated by Django 2.2.7 on 2020-11-24 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0062_auto_20201124_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformnames',
            name='USI',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
