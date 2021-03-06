# Generated by Django 2.2.7 on 2020-09-11 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20200910_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afsl',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.RemoveField(
            model_name='user',
            name='AFSL',
        ),
        migrations.AddField(
            model_name='user',
            name='AFSL',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authorised_reps', to='users.AFSL'),
        ),
    ]
