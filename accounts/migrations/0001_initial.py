# Generated by Django 4.1.7 on 2023-05-24 10:53

import accounts.models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=10, verbose_name='نام')),
                ('last_name', models.CharField(max_length=10, verbose_name='نام خانوادگی')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('phone_number', models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')),
                ('about_me', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='درباره ی من')),
                ('profile_image', models.ImageField(blank=True, default='accounts/defaults/avatar-default.png', null=True, upload_to=accounts.models.user_profile_image_path, verbose_name='عکس پروفایل')),
                ('cover_image', models.ImageField(blank=True, default='accounts/defaults/cover.jpg', null=True, upload_to=accounts.models.user_cover_image_path, verbose_name='عکس کاور')),
                ('background_image', models.ImageField(blank=True, null=True, upload_to=accounts.models.user_background_image_path, verbose_name='عکس پس زمینه')),
                ('is_private', models.BooleanField(default=False, verbose_name='خصوصی')),
                ('is_active', models.BooleanField(default=True)),
                ('is_auther', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('registration_date', models.DateField(auto_now_add=True, verbose_name='تاریخ عضویت')),
                ('last_online', models.DateTimeField(auto_now_add=True, null=True, verbose_name='آخرین انلاین')),
            ],
            options={
                'verbose_name': 'کاربر',
            },
        ),
        migrations.CreateModel(
            name='OTPCodeModel',
            fields=[
                ('phone_number', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='FollowRequestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='self_follow_requests', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_follow_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'درخواست دنبال کردن',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='FollowModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_set', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'دنبال کردن',
            },
        ),
        migrations.CreateModel(
            name='EmojiPackageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heart', models.BooleanField(default=False)),
                ('trophy', models.BooleanField(default=False)),
                ('passion', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'پکیج کاربر',
            },
        ),
        migrations.CreateModel(
            name='BlockModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_by', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'بلاک کردن کاربر',
            },
        ),
        migrations.AddField(
            model_name='usermodel',
            name='blocking',
            field=models.ManyToManyField(related_name='blockers', through='accounts.BlockModel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='emojis_pack',
            field=models.ManyToManyField(related_name='packs_emojis', through='accounts.EmojiPackageModel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='followings',
            field=models.ManyToManyField(related_name='followers', through='accounts.FollowModel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='followings_request',
            field=models.ManyToManyField(related_name='followers_request', through='accounts.FollowRequestModel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='followrequestmodel',
            constraint=models.CheckConstraint(check=models.Q(('from_user', models.F('to_user')), _negated=True), name='any_one_cant_request_to_follows_it_self'),
        ),
        migrations.AlterUniqueTogether(
            name='followrequestmodel',
            unique_together={('from_user', 'to_user')},
        ),
        migrations.AddConstraint(
            model_name='followmodel',
            constraint=models.CheckConstraint(check=models.Q(('to_user', models.F('from_user')), _negated=True), name='any_one_cant_follows_it_self'),
        ),
        migrations.AlterUniqueTogether(
            name='followmodel',
            unique_together={('from_user', 'to_user')},
        ),
        migrations.AlterUniqueTogether(
            name='emojipackagemodel',
            unique_together={('from_user', 'to_user')},
        ),
        migrations.AlterUniqueTogether(
            name='blockmodel',
            unique_together={('from_user', 'to_user')},
        ),
    ]
