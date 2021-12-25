# Generated by Django 4.0 on 2021-12-21 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News_Portal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='author_name',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_rating',
            new_name='rating',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_time',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_rating',
            new_name='rating',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_text',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='author',
            name='author_rating',
        ),
        migrations.AddField(
            model_name='author',
            name='rating',
            field=models.SmallIntegerField(default=0),
        ),
    ]
