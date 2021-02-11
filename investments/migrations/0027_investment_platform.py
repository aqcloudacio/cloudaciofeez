# Generated by Django 2.2.7 on 2020-02-27 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0030_auto_20200221_1540'),
        ('investments', '0026_auto_20200216_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='platforms.Platform'),
        ),
    ]
