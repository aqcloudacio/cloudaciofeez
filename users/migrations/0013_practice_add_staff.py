# Generated by Django 2.2.7 on 2020-05-24 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_pending_practices'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='add_staff',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
