from django.urls import path
from . import api_views


app_name = 'api_accounts'

urlpatterns = [
    path('api-token-auth/', api_views.CustomAuthToken.as_view(), name='obtain_auth_token'),
    path('user-register/', api_views.RegisterUserUserView.as_view(), name='user_register'),
    path('users-list/', api_views.ListUserView.as_view(), name='users-list'),
    path('user-details/<int:pk>/', api_views.UserDetailsView.as_view(), name='user-details'),
    path('user-update/', api_views.UpdateUserView.as_view(), name='user-update'),
    path('user-delete/', api_views.DeleteUserView.as_view(), name='user-delete'),
    path('user-follow/<int:pk>/', api_views.FollowUserView.as_view(), name='user-follow'),
    path('user-unfollow/<int:pk>/', api_views.UnfollowUserView.as_view(), name='user-unfollow'),
    path('follow-request-decision/<int:pk>/', api_views.DecisionFollowRequestView.as_view(),
         name='follow-request-decision'),
    path('user-block/<int:pk>/', api_views.BlockUserView.as_view(), name='block-user'),
    path('user-unblock/<int:pk>/', api_views.UnblockUserView.as_view(), name='block-user'),
    path('user-emojis/<int:pk>/', api_views.UserEmojisView.as_view(), name='user-emojis'),

]
