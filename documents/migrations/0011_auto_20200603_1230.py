# Generated by Django 2.2.7 on 2020-06-03 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_auto_20200602_1658'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='element',
            name='type',
            field=models.CharField(choices=[('rowHeader', 'rowHeader'), ('rowSubheader1', 'rowSubheader1'), ('rowSubheader2', 'rowSubheader2'), ('rowSubtotal', 'rowSubtotal'), ('rowNormal', 'rowNormal'), ('rowTotal', 'rowTotal')], max_length=20),
        ),
        migrations.AlterField(
            model_name='style',
            name='border_width',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='style',
            name='cell_margin_bottom',
            field=models.DecimalField(decimal_places=3, default=56.693, max_digits=8),
        ),
        migrations.AlterField(
            model_name='style',
            name='cell_margin_end',
            field=models.DecimalField(decimal_places=3, default=113.389, max_digits=8),
        ),
        migrations.AlterField(
            model_name='style',
            name='cell_margin_start',
            field=models.DecimalField(decimal_places=3, default=113.389, max_digits=8),
        ),
    ]
