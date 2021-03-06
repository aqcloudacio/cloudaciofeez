# Generated by Django 2.2.7 on 2020-06-02 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20200602_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='content',
        ),
        migrations.RemoveField(
            model_name='document',
            name='structure',
        ),
        migrations.RemoveField(
            model_name='document',
            name='style',
        ),
        migrations.AddField(
            model_name='content',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='structure',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='structures', to='documents.Document'),
        ),
        migrations.AddField(
            model_name='style',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='styles', to='documents.Document'),
        ),
        migrations.AlterField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('Status', 'Status'), ('Product', 'Product'), ('Balance', 'Balance'), ('Investments', 'Investments'), ('Fees', 'Fees'), ('Subtotal', 'Subtotal'), ('Adviser Fee', 'Adviser Fee'), ('Total', 'Total')], max_length=20),
        ),
    ]
