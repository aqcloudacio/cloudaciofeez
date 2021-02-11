# Generated by Django 2.2.7 on 2020-11-23 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0060_auto_20201015_1602'),
        ('scrapes', '0055_auto_20200826_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformScrapeSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(blank=True, max_length=300, null=True)),
                ('root', models.URLField(blank=True, max_length=300, null=True)),
                ('prerender_js', models.BooleanField(default=False)),
                ('pdf', models.BooleanField(default=True)),
                ('pdf_manual', models.BooleanField(default=True)),
                ('pdf_mod_date', models.CharField(default='', max_length=100)),
                ('aa_url', models.CharField(blank=True, max_length=300, null=True)),
                ('platform', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fee_scrape_settings', to='platforms.PlatformNames')),
            ],
        ),
    ]