# Generated by Django 2.2.7 on 2020-06-03 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0016_auto_20200603_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='style',
            name='background_color',
        ),
        migrations.AddField(
            model_name='element',
            name='border_sides',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
