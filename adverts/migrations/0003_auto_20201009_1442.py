# Generated by Django 2.2.7 on 2020-10-09 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0002_auto_20201001_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='show_in_alternative',
            field=models.BooleanField(default=True),
        ),
    ]
