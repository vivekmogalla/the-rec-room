# Generated by Django 4.2.2 on 2023-08-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_alter_notification_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('new_follow', 'New follow'), ('new_chat', 'New chat'), ('post_like', 'Post like'), ('post_comment', 'Post comment'), ('post_tag', 'Post tag')], max_length=50),
        ),
    ]