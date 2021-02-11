# Generated by Django 2.2.7 on 2020-09-21 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0038_theme_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structure',
            name='theme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='structures', to='documents.Theme'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='structure',
            constraint=models.UniqueConstraint(fields=('theme',), name='unique_theme'),
        ),
    ]