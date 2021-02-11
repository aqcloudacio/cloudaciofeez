# Generated by Django 2.2.7 on 2020-06-02 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20200602_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='element',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content', to='documents.Element'),
        ),
        migrations.AddField(
            model_name='content',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='order',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='content',
            name='table_type',
            field=models.CharField(choices=[('Actual', 'Actual'), ('Consolidated', 'Consolidated'), ('AA', 'AA')], default='Actual', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('Status', 'Status'), ('Product', 'Product'), ('Balance', 'Balance'), ('Fees', 'Fees'), ('Subtotal', 'Subtotal'), ('Adviser Fee', 'Adviser Fee'), ('Total', 'Total')], default='Total', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='content',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='document',
            name='content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='documents.Content'),
        ),
        migrations.AddConstraint(
            model_name='content',
            constraint=models.UniqueConstraint(fields=('order', 'table_type'), name='unique_order_per_table'),
        ),
    ]
