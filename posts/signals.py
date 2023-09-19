from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from django.core.files.storage import default_storage
from .models import PostModel, PostEmojiModel, CommentEmojiModel, PostCommentModel
from accounts.models import UserModel


@receiver(post_save, sender=PostModel)
def create_post_emoji(sender, **kwargs):
    post = kwargs['instance']
    if kwargs['created']:
        for user in UserModel.objects.all():
            PostEmojiModel.objects.update_or_create(user=user, post=post)


@receiver(post_save, sender=PostCommentModel)
def create_comment_emoji(sender, **kwargs):
    comment = kwargs['instance']
    if kwargs['created']:
        for user in UserModel.objects.all():
            CommentEmojiModel.objects.update_or_create(user=user, comment=comment)


@receiver(post_save, sender=UserModel)
def create_post_comment_emoji(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        for post in PostModel.objects.all():
            PostEmojiModel.objects.update_or_create(post=post, user=user)
        for comment in PostCommentModel.objects.all():
            CommentEmojiModel.objects.update_or_create(comment=comment, user=user)
