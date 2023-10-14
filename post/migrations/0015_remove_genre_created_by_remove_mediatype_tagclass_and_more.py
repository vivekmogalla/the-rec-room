# Generated by Django 4.2.2 on 2023-08-25 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0014_post_link_genre_post_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='mediatype',
            name='tagClass',
        ),
        migrations.AddField(
            model_name='mediatype',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='media_types', to='post.genre'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='genres',
        ),
        migrations.AddField(
            model_name='post',
            name='genres',
            field=models.ManyToManyField(blank=True, related_name='posts', to='post.genre'),
        ),
    ]