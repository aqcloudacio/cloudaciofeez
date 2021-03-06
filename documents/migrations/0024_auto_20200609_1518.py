# Generated by Django 2.2.7 on 2020-06-09 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0023_auto_20200605_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('Status', 'Status'), ('Product', 'Product'), ('Balance', 'Balance'), ('Investments', 'Investments'), ('One-off Fees Subheader', 'One-off Fees Subheader'), ('Switch Fees', 'Switch Fees'), ('Buy/Sell Fees', 'Buy/Sell Fees'), ('One-off Subtotal', 'One-off Subtotal'), ('Ongoing Fees Subheader', 'Ongoing Fees Subheader'), ('Ongoing Fees Content', 'Ongoing Fees Content'), ('Subtotal', 'Subtotal'), ('Adviser Fee', 'Adviser Fee'), ('Total', 'Total')], max_length=50),
        ),
    ]
