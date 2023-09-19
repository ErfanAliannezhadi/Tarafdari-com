# Generated by Django 4.2.4 on 2023-08-06 13:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statuses', '0004_alter_statuscommentmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuscommentmodel',
            options={'ordering': ['-created'], 'verbose_name': 'کامنت برای استاتوس'},
        ),
        migrations.AlterModelOptions(
            name='statuslikemodel',
            options={'verbose_name': 'لایک برای استاتوس'},
        ),
        migrations.AddField(
            model_name='statusmodel',
            name='likers',
            field=models.ManyToManyField(through='statuses.StatusLikeModel', to=settings.AUTH_USER_MODEL),
        ),
    ]
