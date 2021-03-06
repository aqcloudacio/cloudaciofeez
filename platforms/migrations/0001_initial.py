# Generated by Django 2.2.7 on 2020-01-27 05:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformFamilyGroups',
            fields=[
                ('platformname_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=300, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlatformNames',
            fields=[
                ('platformname_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=300, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('platform_id', models.AutoField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('edited', models.BooleanField()),
                ('template', models.BooleanField()),
                ('platform_type', models.CharField(choices=[('Accumulation', 'Superannuation - Accumulation'), ('Pension', 'Superannuation - Pension'), ('Defined Benefit', 'Superannuation - Defined Benefit'), ('Investment', 'Investment'), ('SMSF', 'Self Managed Super Fund')], default='Accumulation', max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=300)),
                ('notes', models.CharField(blank=True, max_length=400)),
                ('PDS_date', models.DateField(blank=True, null=True)),
                ('PDS_version', models.CharField(blank=True, max_length=50)),
                ('PDS_link', models.URLField(blank=True)),
                ('AA_link', models.URLField(blank=True, null=True)),
                ('ICR_link', models.URLField(blank=True, null=True)),
                ('last_checked', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(blank=True, max_length=50)),
                ('shared_admin_fee', models.BooleanField(default=False)),
                ('allowed_fee_link', models.CharField(choices=[('None', 'No fee linking'), ('Personal', 'Links to own accounts only'), ('Family', 'Links to own direct family only')], default='None', max_length=20)),
                ('maximum_linked_accounts', models.PositiveIntegerField(default=0)),
                ('fee_link_type', models.CharField(choices=[('None', 'No change in admin fee'), ('Combined', 'Admin fee calculated on combined balance'), ('Reduction', 'Admin fee reduced by fixed anmount')], default='None', max_length=20)),
                ('admin_fee_linking_reduction', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('fee_link_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='platforms', to='platforms.PlatformFamilyGroups')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='platforms', to='platforms.PlatformNames')),
            ],
        ),
    ]
