# Generated by Django 2.2.7 on 2020-07-14 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0035_theme_afsl_limitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='table_type',
            field=models.CharField(choices=[('Product', 'Product Advice Table'), ('Actual', 'Fee Table'), ('Consolidated', 'Consolidated Fee Table'), ('AA', 'Asset Allocation Table')], max_length=20),
        ),
    ]
