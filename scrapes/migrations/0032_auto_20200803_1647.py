# Generated by Django 2.2.7 on 2020-08-03 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0031_auto_20200803_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='CamelotSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_pages', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='investmentscrapesettings',
            name='aa_pdf_pages',
        ),
        migrations.RemoveField(
            model_name='investmentscrapesettings',
            name='fee_pdf_pages',
        ),
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='aa_camelot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aa_settings', to='scrapes.CamelotSettings'),
        ),
        migrations.AddField(
            model_name='investmentscrapesettings',
            name='fee_camelot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fee_settings', to='scrapes.CamelotSettings'),
        ),
    ]
