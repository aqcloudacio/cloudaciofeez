# Generated by Django 2.2.7 on 2020-05-26 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20200526_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]