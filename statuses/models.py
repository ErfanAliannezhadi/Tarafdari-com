import os
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
from accounts.models import UserModel


def status_file_path(instance, filename):
    return f'statuses/status_{instance.pk}/{filename}'


IMAGE_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
VIDEO_FILE_EXTENSIONS = ['.mp4', '.mkv', '.mvw', '.mpeg']
AUDIO_FILE_EXTENSIONS = ['.mp3', '.wav']


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = IMAGE_FILE_EXTENSIONS + VIDEO_FILE_EXTENSIONS + AUDIO_FILE_EXTENSIONS
    if not ext.lower() in valid_extensions:
        raise ValidationError('فرمت فایل غیرقابل قبول است.')


class StatusModel(models.Model):
    from_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_statuses')
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='profile_statuses')
    likers = models.ManyToManyField(UserModel, through='StatusLikeModel')
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name='محتوا')
    file = models.FileField(upload_to=status_file_path, verbose_name='رسانه', blank=True, null=True,
                            validators=[validate_file_extension])
    is_private = models.BooleanField(default=False, verbose_name='خصوصی')
    is_pin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.content[:15]} ....'

    @property
    def is_message(self):
        return self.from_user != self.to_user

    def type_of_file(self):
        ext = os.path.splitext(self.file.path)[1]
        if ext in IMAGE_FILE_EXTENSIONS:
            return 'image'
        if ext in VIDEO_FILE_EXTENSIONS:
            return 'video'
        if ext in AUDIO_FILE_EXTENSIONS:
            return 'audio'

    def get_absolute_url(self):
        return reverse('statuses:status_detail', kwargs={'status_pk': self.pk})

    class Meta:
        verbose_name = 'استاتوس'
        ordering = ['-is_pin', '-created']
        constraints = [
            models.CheckConstraint(check=(~models.Q(to_user=models.F('from_user')) | models.Q(is_private=False)),
                                   name='only messages can be private'),
            models.CheckConstraint(check=(models.Q(to_user=models.F('from_user')) | models.Q(is_pin=False)),
                                   name='only statuses can be pin')
        ]


class StatusCommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusModel, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        verbose_name = 'کامنت برای استاتوس'
        ordering = ['created']


class StatusLikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusModel, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'لایک برای استاتوس'
        unique_together = ['user', 'status']
