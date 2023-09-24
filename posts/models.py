import os
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from accounts.models import UserModel
from teams.models import TeamModel
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


def post_file_path(instance, filename):
    return f'posts/post_{instance.pk}/{filename}'


IMAGE_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
VIDEO_FILE_EXTENSIONS = ['.mp4', '.mkv', '.mvw', '.mpeg']
AUDIO_FILE_EXTENSIONS = ['.mp3', '.wav']


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = IMAGE_FILE_EXTENSIONS + VIDEO_FILE_EXTENSIONS + AUDIO_FILE_EXTENSIONS
    if not ext.lower() in valid_extensions:
        raise ValidationError('فرمت فایل غیرقابل قبول است.')


class PostModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    auther = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts', verbose_name='نویسنده')
    created = models.DateTimeField(auto_now=True, verbose_name='تاریخ')
    content = RichTextField(verbose_name='محتوا')
    file = models.FileField(upload_to=post_file_path, verbose_name='رسانه', blank=True, null=True,
                            validators=[validate_file_extension])
    numbers_of_seen = models.IntegerField(default=0, verbose_name='تعداد مشاهدات')
    teams = models.ManyToManyField(TeamModel, verbose_name='تیم ها', blank=True)
    tags = TaggableManager(verbose_name='تگ ها', blank=True)
    is_news = models.BooleanField(verbose_name='خبر')

    def type_of_file(self):
        ext = os.path.splitext(self.file.path)[1]
        if ext in IMAGE_FILE_EXTENSIONS:
            return 'image'
        if ext in VIDEO_FILE_EXTENSIONS:
            return 'video'
        if ext in AUDIO_FILE_EXTENSIONS:
            return 'audio'

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.pk})

    def number_of_like_emojis(self):
        return self.emojis.filter(like_emoji=True).count()

    def number_of_dislike_emojis(self):
        return self.emojis.filter(dislike_emoji=True).count()

    def number_of_heart_emojis(self):
        return self.emojis.filter(heart_emoji=True).count()

    def likers(self):
        return [emoji.user for emoji in self.emojis.filter(like_emoji=True)]

    def dislikers(self):
        return [emoji.user for emoji in self.emojis.filter(dislike_emoji=True)]

    def hearters(self):
        return [emoji.user for emoji in self.emojis.filter(heart_emoji=True)]

    class Meta:
        verbose_name = 'پست'
        ordering = ['-created']


class PostCommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    content = models.TextField(verbose_name='محتوا')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True,
                              verbose_name='پاسخ به')
    is_reply = models.BooleanField(default=False, verbose_name='ریپلای است؟')

    def number_of_like_emojis(self):
        return self.emojis.filter(like_emoji=True).count()

    def number_of_dislike_emojis(self):
        return self.emojis.filter(dislike_emoji=True).count()

    def likers(self):
        return [emoji.user for emoji in self.emojis.filter(like_emoji=True)]

    def dislikers(self):
        return [emoji.user for emoji in self.emojis.filter(dislike_emoji=True)]

    class Meta:
        verbose_name = 'کامنت'
        ordering = ['-created']


class PostEmojiModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='emojis')
    like_emoji = models.BooleanField(default=False)
    dislike_emoji = models.BooleanField(default=False)
    heart_emoji = models.BooleanField(default=False)

    def reverse_like(self):
        self.like_emoji = not self.like_emoji
        self.save()

    def reverse_dislike(self):
        self.dislike_emoji = not self.dislike_emoji
        self.save()

    def reverse_heart(self):
        self.heart_emoji = not self.heart_emoji
        self.save()


class CommentEmojiModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostCommentModel, on_delete=models.CASCADE, related_name='emojis')
    like_emoji = models.BooleanField(default=False)
    dislike_emoji = models.BooleanField(default=False)

    def reverse_like(self):
        self.like_emoji = not self.like_emoji
        self.save()

    def reverse_dislike(self):
        self.dislike_emoji = not self.dislike_emoji
        self.save()
