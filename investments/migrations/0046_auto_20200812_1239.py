# Generated by Django 2.2.7 on 2020-08-12 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0045_auto_20200729_1459'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='assetallocationname',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_aa_name'),
        ),
    ]
