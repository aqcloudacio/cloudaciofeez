# Generated by Django 2.2.7 on 2020-07-21 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0003_remove_investmentscrape_aa_link_root'),
    ]

    operations = [
        migrations.CreateModel(
            name='AARoot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root', models.URLField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]