# Generated by Django 2.2.7 on 2020-06-03 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0017_auto_20200603_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='element',
            name='border_sides',
        ),
        migrations.RemoveField(
            model_name='style',
            name='border_bottom',
        ),
        migrations.RemoveField(
            model_name='style',
            name='border_end',
        ),
        migrations.RemoveField(
            model_name='style',
            name='border_inner_horizontal',
        ),
        migrations.RemoveField(
            model_name='style',
            name='border_inner_vertical',
        ),
        migrations.RemoveField(
            model_name='style',
            name='border_start',
        ),
        migrations.RemoveField(
            model_name='style',
            name='border_top',
        ),
        migrations.AddField(
            model_name='style',
            name='border_sides',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
