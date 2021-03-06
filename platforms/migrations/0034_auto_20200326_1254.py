# Generated by Django 2.2.7 on 2020-03-26 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0033_platformfees_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='custom_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='platform',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='platforms', to='platforms.PlatformNames'),
        ),
    ]
