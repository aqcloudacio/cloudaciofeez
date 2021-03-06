# Generated by Django 2.2.7 on 2020-02-07 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0017_auto_20200131_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='portfolios.Portfolio'),
        ),
    ]
