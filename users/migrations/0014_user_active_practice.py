# Generated by Django 2.2.7 on 2020-05-24 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_practice_add_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_practice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='active_staff', to='users.Practice'),
        ),
    ]