# Generated by Django 2.2.7 on 2020-06-10 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0027_remove_structure_display_one_off_fees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='structure',
            name='display_investment_names',
        ),
    ]
