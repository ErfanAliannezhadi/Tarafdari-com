from django.urls import path
from . import api_views

app_name = 'api_statuses'

urlpatterns = [
    path('user/<int:pk>/statuses/', api_views.UserStatusesListView.as_view(), name='user-statuses-list'),
    path('user/<int:pk>/receive-messages/', api_views.UserReceiverMessageListView.as_view(),
         name='user-receive-messages-list'),
    path('user/<int:pk>/deliver-messages/', api_views.UserDeliverMessageListView.as_view(),
         name='user-deliver-messages-list'),
    path('create-status/', api_views.CreateStatusView.as_view(), name='create-status'),
    path('update-status/<int:pk>/', api_views.UpdateStatusView.as_view(), name='update-status'),
    path('delete-status/<int:pk>/', api_views.DeleteStatusView.as_view(), name='delete-status'),
    path('retrieve-status/<int:pk>/', api_views.RetrieveStatusView.as_view(), name='retrieve-status'),
    path('status/<int:pk>/comments-list/', api_views.StatusCommentsListView.as_view(), name='status-comments'),
    path('status/<int:pk>/create-comment/', api_views.CreateCommentView.as_view(), name='create-comment'),
    path('comment/<int:pk>/delete/', api_views.DeleteCommentView.as_view(), name='delete-comment'),
    path('status/<int:pk>/like/', api_views.StatusLikeView.as_view(), name='like-status'),
    path('status/<int:pk>/unlike/', api_views.StatusUnlikeView.as_view(), name='unlike-status'),
]
