# Generated by Django 4.2.2 on 2023-08-15 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notification_body_notification_is_read'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('created_at',)},
        ),
    ]