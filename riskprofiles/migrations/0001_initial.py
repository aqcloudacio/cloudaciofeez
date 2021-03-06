# Generated by Django 2.2.7 on 2020-03-07 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_remove_user_allowed_portfolios'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('AFSL_limitation', models.ManyToManyField(blank=True, related_name='risk_profiles', to='users.AFSL')),
            ],
        ),
        migrations.CreateModel(
            name='RiskProfileAAName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RiskProfileAA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=6, default=0, max_digits=7)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='riskprofiles.RiskProfileAAName')),
                ('riskprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='riskprofiles.RiskProfile')),
            ],
        ),
    ]
