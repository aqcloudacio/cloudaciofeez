# Generated by Django 2.2.7 on 2020-06-24 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_user_active_theme'),
        ('documents', '0034_auto_20200618_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='AFSL_limitation',
            field=models.ManyToManyField(blank=True, related_name='themes', to='users.AFSL'),
        ),
    ]
