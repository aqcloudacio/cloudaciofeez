# Generated by Django 2.2.7 on 2020-05-15 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0044_auto_20200512_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
