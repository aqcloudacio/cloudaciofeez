# Generated by Django 2.2.7 on 2020-02-09 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0015_auto_20200208_1302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='platformtierpercs',
            options={'ordering': ['-percentage']},
        ),
        migrations.AlterModelOptions(
            name='platformtierthresholds',
            options={'ordering': ['threshold']},
        ),
        migrations.AddField(
            model_name='platformfees',
            name='ORR_levy_cap',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
