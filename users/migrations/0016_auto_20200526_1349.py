# Generated by Django 2.2.7 on 2020-05-26 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=300)),
                ('type', models.CharField(max_length=100)),
                ('read', models.BooleanField(default=False)),
                ('to', models.CharField(max_length=100)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('practice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='users.Practice')),
                ('target', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Notifications',
        ),
    ]
