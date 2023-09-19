from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/create/comment/', views.CreateCommentView.as_view(), name='post_comment_create'),
    path('post/<int:pk>/emoji-package/', views.PostEmojiPackageView.as_view(), name='post_emoji_package'),
    path('comment/<int:pk>/emoji-package/', views.CommentEmojiPackageView.as_view(), name='comment_emoji_package'),
    path('comment/<int:pk>/reply/', views.CommentReplyView.as_view(), name='comment_reply_create'),
    path('create-post/', views.CreatePostView.as_view(), name='create_post')
]
