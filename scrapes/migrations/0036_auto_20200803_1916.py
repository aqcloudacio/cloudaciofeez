# Generated by Django 2.2.7 on 2020-08-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0035_auto_20200803_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camelotsettings',
            name='row_tol',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
