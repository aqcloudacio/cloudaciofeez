# Generated by Django 2.2.7 on 2020-09-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0046_auto_20200812_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentclass',
            name='category',
            field=models.CharField(blank=True, choices=[('MF', 'Managed Fund'), ('MA', 'Managed Account'), ('LISTED', 'Australian Listed Asset'), ('OTHER', 'Other Asset')], max_length=100, null=True),
        ),
    ]
