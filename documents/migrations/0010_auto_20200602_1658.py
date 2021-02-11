# Generated by Django 2.2.7 on 2020-06-02 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_auto_20200602_1658'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='content',
            constraint=models.UniqueConstraint(fields=('order', 'table_type', 'theme'), name='unique_order_per_table'),
        ),
    ]