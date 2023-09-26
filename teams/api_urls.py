from django.urls import path
from . import api_views

app_name = 'api_teams'

urlpatterns = [
    path('user-follow-team/<str:pk>/', api_views.UserFollowTeamView.as_view(), name='user-follow-team'),
    path('user-unfollow-team/<str:pk>/', api_views.UserUnfollowTeamView.as_view(), name='user-unfollow-team'),
]
