# Generated by Django 4.2.2 on 2023-08-12 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_post_media_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediatype',
            name='tagClass',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]