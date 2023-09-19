# Generated by Django 4.2.4 on 2023-09-16 08:12

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('posts', '0002_postemojimodel_commentemojimodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcommentmodel',
            options={'ordering': ['-created'], 'verbose_name': 'کامنت'},
        ),
        migrations.AlterModelOptions(
            name='postmodel',
            options={'ordering': ['-created'], 'verbose_name': 'پست'},
        ),
        migrations.AlterField(
            model_name='commentemojimodel',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emojis', to='posts.postcommentmodel'),
        ),
        migrations.AlterField(
            model_name='postemojimodel',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emojis', to='posts.postmodel'),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='محتوا'),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='تگ ها'),
        ),
    ]
