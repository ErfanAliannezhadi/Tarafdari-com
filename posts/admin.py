from django.contrib import admin
from .models import PostModel, PostCommentModel, PostEmojiModel, CommentEmojiModel

admin.site.register(PostModel)
admin.site.register(PostCommentModel)
admin.site.register(PostEmojiModel)
admin.site.register(CommentEmojiModel)
