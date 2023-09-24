from django.urls import path
from . import api_views

app_name = 'api_posts'

urlpatterns = [
    path('posts-list/', api_views.PostListView.as_view(), name='posts-list'),
    path('post-create/', api_views.PostCreateView.as_view(), name='post-create'),
    path('post-details/<int:pk>/', api_views.PostDetailView.as_view(), name='post-details'),
    path('post-update/<int:pk>/', api_views.PostUpdateView.as_view(), name='post-update'),
    path('post-delete/<int:pk>/', api_views.PostDeleteView.as_view(), name='post-delete'),
    path('post-emojis/<int:pk>/', api_views.PostEmojiView.as_view(), name='post-emojis'),
    path('post-comments-list/<int:pk>/', api_views.PostCommentsListView.as_view(), name='post-comments-list'),
    path('comment-replies-list/<int:pk>/', api_views.CommentRepliesView.as_view(), name='comment-replies-list'),
    path('comment-create/<int:pk>/', api_views.CreateCommentView.as_view(), name='comment-create'),
    path('comment-update/<int:pk>/', api_views.UpdateCommentView.as_view(), name='comment-update'),
    path('comment-delete/<int:pk>/', api_views.DeleteCommentView.as_view(), name='comment-delete'),
    path('comment-emojis/<int:pk>/', api_views.CommentEmojisView.as_view(), name='comment-emojis'),

]
