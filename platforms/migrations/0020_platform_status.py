# Generated by Django 2.2.7 on 2020-02-11 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0019_auto_20200210_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='status',
            field=models.CharField(choices=[('Current', 'Current'), ('Recommended', 'Recommended'), ('Alternative', 'Alternative')], default='Current', max_length=100),
        ),
    ]
