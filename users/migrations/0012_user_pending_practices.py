# Generated by Django 2.2.7 on 2020-05-23 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_practice_model_portfolios'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pending_practices',
            field=models.ManyToManyField(blank=True, related_name='pending_staff', to='users.Practice'),
        ),
    ]