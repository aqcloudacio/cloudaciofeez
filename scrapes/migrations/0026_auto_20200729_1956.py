# Generated by Django 2.2.7 on 2020-07-29 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0025_investmentscrapesettings_aa_slugify_path_no_hyphens'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='fee_pdf',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='investmentscrape',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scrapes', to='investments.InvestmentName'),
        ),
    ]